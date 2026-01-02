import { AlertTriangle } from 'lucide-react';

function RegretWarningBox({ regretData }) {
    if (!regretData || !regretData.output) return null;

    const riskLevel = regretData.output.risk_level || 'Medium';
    const scenarios = regretData.output.downside_scenarios || [];

    // Only show if risk is Medium or High
    if (riskLevel === 'Low') return null;

    return (
        <div className="relative group">
            {/* 3D Base layers */}
            <div className="absolute inset-0 bg-gradient-to-br from-orange-200 to-red-200 rounded-xl blur-xl opacity-40 group-hover:opacity-60 transition-opacity"></div>
            <div className="absolute inset-1 bg-gradient-to-br from-orange-100 to-red-100 rounded-xl blur-lg opacity-50"></div>

            {/* Main content */}
            <div className="relative bg-gradient-to-br from-orange-50 to-red-50 border-2 border-orange-300 rounded-xl p-6 shadow-lg transform transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl">
                {/* 3D accent bar */}
                <div className="absolute left-0 top-0 bottom-0 w-2 bg-gradient-to-b from-orange-500 to-red-500 rounded-l-xl shadow-lg"></div>

                <div className="flex items-start gap-4 ml-2">
                    {/* Icon with 3D effect */}
                    <div className="relative flex-shrink-0">
                        <div className="absolute inset-0 bg-orange-400 rounded-full blur-md opacity-50"></div>
                        <div className="relative bg-gradient-to-br from-orange-400 to-red-500 p-3 rounded-full shadow-lg">
                            <AlertTriangle className="w-6 h-6 text-white" />
                        </div>
                    </div>

                    <div className="flex-1">
                        <h3 className="text-lg font-bold text-gray-900 mb-2 flex items-center gap-2">
                            Regret Warning: {riskLevel} Risk
                        </h3>

                        <p className="text-gray-700 text-sm mb-4">
                            Our AI has identified potential downside scenarios. Consider these before investing:
                        </p>

                        {scenarios.length > 0 && (
                            <div className="space-y-2">
                                {scenarios.slice(0, 3).map((scenario, idx) => (
                                    <div key={idx} className="flex items-start gap-2 bg-white/60 p-3 rounded-lg border border-orange-200 shadow-sm">
                                        <span className="text-orange-600 font-bold text-sm">⚠️</span>
                                        <span className="text-gray-800 text-sm">{scenario}</span>
                                    </div>
                                ))}
                            </div>
                        )}

                        <div className="mt-4 p-3 bg-white/80 rounded-lg border border-orange-200">
                            <p className="text-xs text-gray-600 italic">
                                💡 <strong>Emotional Preparation:</strong> If this investment drops 20%, can you hold through the fear? Our Regret Agent helps you prepare mentally for worst-case scenarios.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default RegretWarningBox;
