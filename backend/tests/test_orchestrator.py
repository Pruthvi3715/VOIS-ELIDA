"""
Tests for the orchestrator module.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.orchestrator import FinancialOrchestrator
from app.core.exceptions import OrchestrationException


class TestOrchestrator:
    """Tests for the FinancialOrchestrator."""
    
    def test_orchestrator_initialization(self):
        """Orchestrator should initialize with empty cache."""
        orchestrator = FinancialOrchestrator()
        assert orchestrator.current_asset_data == {}
    
    @patch('app.agents.scout.scout_agent.collect_data')
    @patch('app.services.rag_service.rag_service.add_documents')
    @patch('app.services.rag_service.rag_service.delete_by_asset')
    def test_ingest_asset_success(self, mock_delete, mock_add, mock_collect):
        """Ingestion should collect and store data."""
        mock_delete.return_value = 0
        mock_collect.return_value = {
            "financials": {"price": 100},
            "macro": {"rbi_rate": 6.5},
            "technicals": {"rsi": 50},
            "news": []
        }
        mock_add.return_value = None
        
        orchestrator = FinancialOrchestrator()
        result = orchestrator.ingest_asset("TEST")
        
        assert result["status"] == "success"
        assert result["asset_id"] == "TEST"
        mock_collect.assert_called_once_with("TEST")
    
    @patch('app.agents.scout.scout_agent.collect_data')
    def test_ingest_asset_failure(self, mock_collect):
        """Ingestion should raise OrchestrationException on failure."""
        mock_collect.side_effect = Exception("API Error")
        
        orchestrator = FinancialOrchestrator()
        
        with pytest.raises(OrchestrationException) as exc_info:
            orchestrator.ingest_asset("TEST")
        
        assert "ingestion" in str(exc_info.value)


class TestParallelExecution:
    """Tests for parallel agent execution."""
    
    @patch('app.services.rag_service.rag_service.query')
    @patch('app.agents.quant.quant_agent.run')
    @patch('app.agents.macro.macro_agent.run')
    @patch('app.agents.philosopher.philosopher_agent.run')
    @patch('app.agents.regret.regret_agent.run')
    @patch('app.agents.coach.coach_agent.run')
    @patch('app.services.match_score_service.match_score_service.calculate_match_score')
    def test_agents_run_in_parallel(
        self, mock_match, mock_coach, mock_regret, mock_phil, mock_macro, mock_quant, mock_rag
    ):
        """All 4 agents should be invoked."""
        # Setup mocks
        mock_rag.return_value = {"documents": [[]], "metadatas": [[]]}
        
        mock_result = {"score": 50, "analysis": "Test", "confidence": 75}
        mock_quant.return_value = mock_result
        mock_macro.return_value = mock_result
        mock_phil.return_value = mock_result
        mock_regret.return_value = mock_result
        mock_coach.return_value = {"verdict": "HOLD", "score": 50}
        
        mock_match.return_value = MagicMock(
            match_score=50,
            recommendation="HOLD",
            action_if_owned="Hold",
            action_if_not_owned="Wait",
            fit_reasons=["Test reason"],
            concern_reasons=["Test concern"],
            summary="Test summary",
            breakdown=MagicMock(
                fundamental_score=50,
                macro_score=50,
                philosophy_score=50,
                risk_score=50,
                dna_match_score=50
            )
        )
        
        orchestrator = FinancialOrchestrator()
        orchestrator.current_asset_data["TEST"] = {"financials": {}, "technicals": {}}
        
        # Run retrieval (which includes parallel agents)
        result = orchestrator.retrieve_context("test query", "TEST")
        
        # Verify all agents were called
        mock_quant.assert_called_once()
        mock_macro.assert_called_once()
        mock_phil.assert_called_once()
        mock_regret.assert_called_once()


class TestMatchScore:
    """Tests for match score calculation."""
    
    def test_match_score_range(self):
        """Match score should be between 0-100."""
        from app.services.match_score_service import match_score_service
        from app.models.investor_dna import DEFAULT_INVESTOR_DNA
        
        agent_results = {
            "quant": {"score": 75},
            "macro": {"output": {"trend": "Positive"}},
            "philosopher": {"score": 80},
            "regret": {"output": {"risk_level": "Low"}}
        }
        
        asset_data = {
            "financials": {"sector": "Technology", "pe_ratio": 25}
        }
        
        result = match_score_service.calculate_match_score(
            agent_results=agent_results,
            asset_data=asset_data,
            investor_dna=DEFAULT_INVESTOR_DNA
        )
        
        assert 0 <= result.match_score <= 100
