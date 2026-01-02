"""
Screener.in Scraper Service
Fetches India-specific financial metrics not available in Yahoo Finance:
- ROCE (Return on Capital Employed)
- Promoter Holding %
- Book Value (more accurate for Indian stocks)
- Sales Growth (5yr, 10yr)
- Profit Growth (5yr, 10yr)
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re


class ScreenerService:
    """
    Scrapes financial data from Screener.in for Indian stocks.
    """
    
    BASE_URL = "https://www.screener.in/company/{symbol}/"
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    def get_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch data from Screener.in for a given symbol.
        
        Args:
            symbol: Stock symbol (e.g., "SUZLON" for SUZLON.NS)
        
        Returns:
            Dictionary with Screener.in data
        """
        # Convert Yahoo symbol to Screener format
        screener_symbol = self._convert_symbol(symbol)
        
        try:
            url = self.BASE_URL.format(symbol=screener_symbol)
            response = requests.get(url, headers=self.HEADERS, timeout=10)
            
            if response.status_code != 200:
                return {"error": f"Failed to fetch: HTTP {response.status_code}"}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            data = {
                "source": "Screener.in",
                "symbol": symbol,
                "screener_symbol": screener_symbol,
            }
            
            # Extract key ratios from the ratios section
            data.update(self._extract_ratios(soup))
            
            # Extract shareholding pattern
            data.update(self._extract_shareholding(soup))
            
            # Extract growth metrics
            data.update(self._extract_growth(soup))
            
            return data
            
        except requests.exceptions.Timeout:
            return {"error": "Request timeout", "source": "Screener.in"}
        except Exception as e:
            return {"error": str(e), "source": "Screener.in"}
    
    def _convert_symbol(self, yahoo_symbol: str) -> str:
        """Convert Yahoo symbol to Screener format."""
        # Remove exchange suffix (.NS, .BO)
        if yahoo_symbol.endswith(".NS") or yahoo_symbol.endswith(".BO"):
            return yahoo_symbol[:-3]
        return yahoo_symbol
    
    def _extract_ratios(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract key financial ratios."""
        ratios = {}
        
        try:
            # Find the ratios section
            ratio_list = soup.find('ul', {'id': 'top-ratios'})
            if ratio_list:
                items = ratio_list.find_all('li')
                for item in items:
                    name_elem = item.find('span', {'class': 'name'})
                    value_elem = item.find('span', {'class': 'number'})
                    
                    if name_elem and value_elem:
                        name = name_elem.get_text(strip=True).lower()
                        value = self._parse_value(value_elem.get_text(strip=True))
                        
                        if 'market cap' in name:
                            ratios['screener_market_cap'] = value
                        elif 'stock p/e' in name:
                            ratios['screener_pe'] = value
                        elif 'book value' in name:
                            ratios['screener_book_value'] = value
                        elif 'roce' in name:
                            ratios['roce'] = value
                        elif 'roe' in name:
                            ratios['screener_roe'] = value
                        elif 'dividend yield' in name:
                            ratios['screener_dividend_yield'] = value
                        elif 'face value' in name:
                            ratios['face_value'] = value
        except Exception as e:
            ratios['ratio_error'] = str(e)
        
        return ratios
    
    def _extract_shareholding(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract shareholding pattern."""
        shareholding = {}
        
        try:
            # Look for shareholding section
            sh_section = soup.find('div', {'id': 'shareholding'})
            if sh_section:
                # Find latest holding data
                table = sh_section.find('table')
                if table:
                    rows = table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['th', 'td'])
                        if len(cells) >= 2:
                            label = cells[0].get_text(strip=True).lower()
                            value = cells[-1].get_text(strip=True)  # Latest column
                            
                            if 'promoter' in label:
                                shareholding['promoter_holding'] = self._parse_value(value)
                            elif 'fii' in label or 'foreign' in label:
                                shareholding['fii_holding'] = self._parse_value(value)
                            elif 'dii' in label or 'domestic' in label:
                                shareholding['dii_holding'] = self._parse_value(value)
                            elif 'public' in label:
                                shareholding['public_holding'] = self._parse_value(value)
        except Exception as e:
            shareholding['shareholding_error'] = str(e)
        
        return shareholding
    
    def _extract_growth(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract growth metrics."""
        growth = {}
        
        try:
            # Look for compounded growth section
            tables = soup.find_all('table', {'class': 'ranges-table'})
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['th', 'td'])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        
                        # Look for 5yr and 10yr columns
                        for i, cell in enumerate(cells[1:], 1):
                            value = cell.get_text(strip=True)
                            
                            if 'sales' in label or 'revenue' in label:
                                if i == 1:
                                    growth['sales_growth_5yr'] = self._parse_value(value)
                            elif 'profit' in label:
                                if i == 1:
                                    growth['profit_growth_5yr'] = self._parse_value(value)
        except Exception as e:
            growth['growth_error'] = str(e)
        
        return growth
    
    def _parse_value(self, text: str) -> Optional[float]:
        """Parse a text value into a number."""
        if not text or text == '--':
            return None
        
        try:
            # Remove commas and percentage signs
            clean = text.replace(',', '').replace('%', '').strip()
            
            # Handle Cr (Crore) suffix
            if 'Cr' in clean:
                num = float(clean.replace('Cr', '').strip())
                return num  # Keep in Crores for Indian context
            
            return float(clean)
        except ValueError:
            return None


# Singleton instance
screener_service = ScreenerService()
