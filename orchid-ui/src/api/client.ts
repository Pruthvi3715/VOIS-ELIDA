const BASE_URL = ''

interface ApiError {
  message: string
  status: number
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ApiError = {
      message: `HTTP ${response.status}: ${response.statusText}`,
      status: response.status
    }
    throw error
  }
  return response.json()
}

export const api = {
  async getMarketData(ticker: string) {
    const res = await fetch(`${BASE_URL}/market-data/${ticker}`)
    return handleResponse<any>(res)
  },

  async analyzeStock(ticker: string, userId: string = 'default_user', demo: boolean = true) {
    const res = await fetch(`${BASE_URL}/analyze/${ticker}?user_id=${userId}&demo=${demo}`)
    return handleResponse<any>(res)
  },

  analyzeStockStream(ticker: string, onUpdate: (data: any) => void, onComplete: (result: any) => void) {
    const eventSource = new EventSource(`${BASE_URL}/api/analyze-stream/${ticker}`)
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'complete') {
        onComplete(data.result)
        eventSource.close()
      } else {
        onUpdate(data)
      }
    }
    
    eventSource.onerror = () => {
      eventSource.close()
    }
    
    return () => eventSource.close()
  },

  async getDemoTickers() {
    const res = await fetch(`${BASE_URL}/api/demo/tickers`)
    return handleResponse<{ tickers: string[], display_names: string[] }>(res)
  },

  async compareStocks(tickers: string[]) {
    const res = await fetch(`${BASE_URL}/api/compare?tickers=${tickers.join(',')}`)
    return handleResponse<any>(res)
  },

  async getProfile(userId: string = 'default_user') {
    const res = await fetch(`${BASE_URL}/api/v1/profile/${userId}`)
    return handleResponse<any>(res)
  },

  async saveProfile(userId: string, profile: any) {
    const res = await fetch(`${BASE_URL}/api/v1/profile/${userId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile)
    })
    return handleResponse<any>(res)
  },

  async getHistory(userId: string = 'default_user') {
    const res = await fetch(`${BASE_URL}/api/history/${userId}`)
    return handleResponse<any>(res)
  },

  async chat(message: string, context?: any) {
    const res = await fetch(`${BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, context })
    })
    return handleResponse<any>(res)
  }
}
