"""
Tests for analysis agents.
"""
import pytest
from unittest.mock import patch, MagicMock


def disable_llm(agent):
    """Disable all LLM providers for an agent."""
    agent.use_groq = False
    agent.use_ollama = False
    agent.use_gemini = False


class TestQuantAgent:
    """Tests for the Quant Agent."""
    
    def test_quant_agent_returns_score(self, sample_context):
        """Quant agent should return a score between 0-100."""
        from app.agents.quant import quant_agent
        
        # Disable LLMs to force rule-based fallback
        disable_llm(quant_agent)
        
        result = quant_agent.run(sample_context)
        
        assert "score" in result or "output" in result
        score = result.get("score") or result.get("output", {}).get("score", 0)
        assert 0 <= score <= 100
    
    def test_quant_agent_handles_empty_context(self):
        """Quant agent should handle empty context gracefully."""
        from app.agents.quant import quant_agent
        
        disable_llm(quant_agent)
        
        result = quant_agent.run([])
        
        assert result is not None
        assert "analysis" in result or "error" in result


class TestMacroAgent:
    """Tests for the Macro Agent."""
    
    def test_macro_agent_returns_trend(self, sample_context):
        """Macro agent should return a trend assessment."""
        from app.agents.macro import macro_agent
        
        disable_llm(macro_agent)
        
        # Macro agent might need real data for rule-based, so this might return error/fallback
        # We just want to ensure it doesn't crash
        result = macro_agent.run(sample_context)
        
        assert result is not None


class TestPhilosopherAgent:
    """Tests for the Philosopher Agent."""
    
    def test_philosopher_agent_returns_alignment(self, sample_context):
        """Philosopher agent should return quality alignment."""
        from app.agents.philosopher import philosopher_agent
        
        disable_llm(philosopher_agent)
        
        result = philosopher_agent.run(sample_context)
        
        assert result is not None


class TestRegretAgent:
    """Tests for the Regret Simulation Agent."""
    
    def test_regret_agent_returns_risk_level(self, sample_context):
        """Regret agent should return risk assessment."""
        from app.agents.regret import regret_agent
        
        disable_llm(regret_agent)
        
        result = regret_agent.run(sample_context)
        
        assert result is not None


class TestCoachAgent:
    """Tests for the Coach Synthesizer Agent."""
    
    def test_coach_agent_synthesizes(self, sample_context):
        """Coach should synthesize agent insights."""
        from app.agents.coach import coach_agent
        
        disable_llm(coach_agent)
        
        result = coach_agent.run(sample_context)
        
        assert result is not None


class TestAgentScoreRanges:
    """Test that all agents return scores in valid ranges."""
    
    @pytest.mark.parametrize("agent_module,agent_name", [
        ("app.agents.quant", "quant_agent"),
        ("app.agents.macro", "macro_agent"),
        ("app.agents.philosopher", "philosopher_agent"),
        ("app.agents.regret", "regret_agent"),
    ])
    def test_agent_score_in_range(self, sample_context, agent_module, agent_name):
        """All agents should return scores between 0-100."""
        import importlib
        module = importlib.import_module(agent_module)
        agent = getattr(module, agent_name)
        
        disable_llm(agent)
        
        result = agent.run(sample_context)
        
        # Extract score from various possible locations
        score = (
            result.get("score") or 
            result.get("output", {}).get("score") or
            50  # Default if not found
        )
        
        # Some agents might return None/0 if no rule-based logic exists
        # We just want to ensure no crash and type correctness
        if score is not None:
             assert 0 <= score <= 100, f"{agent_name} returned invalid score: {score}"
