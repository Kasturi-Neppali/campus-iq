import React, { useState } from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle, Info, X, Sparkles } from 'lucide-react';

export default function RiskBadge({ riskLevel, riskScore, contributingFactors = [], recommendations = [] }) {
  const [modalOpen, setModalOpen] = useState(false);

  const getStyle = () => {
    switch (riskLevel) {
      case 'HIGH':
        return {
          pill: 'bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100',
          dot: 'bg-rose-500',
          icon: ShieldAlert,
          title: 'High Academic Risk',
          color: 'rose',
        };
      case 'MEDIUM':
        return {
          pill: 'bg-amber-50 text-amber-700 border-amber-200 hover:bg-amber-100',
          dot: 'bg-amber-500',
          icon: AlertTriangle,
          title: 'Medium Academic Risk',
          color: 'amber',
        };
      case 'LOW':
      default:
        return {
          pill: 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100',
          dot: 'bg-emerald-500',
          icon: ShieldCheck,
          title: 'Low Academic Risk',
          color: 'emerald',
        };
    }
  };

  const style = getStyle();
  const Icon = style.icon;

  return (
    <>
      <button
        onClick={() => setModalOpen(true)}
        className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border transition cursor-pointer shadow-2xs ${style.pill}`}
        title="Click to view Machine Learning Risk Diagnostics"
      >
        <span className={`w-2 h-2 rounded-full ${style.dot} animate-pulse`} />
        <span>{riskLevel} RISK</span>
        <Info className="w-3.5 h-3.5 opacity-70 ml-0.5" />
      </button>

      {/* Explainable AI Modal */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className={`p-3 rounded-xl bg-${style.color}-100 text-${style.color}-600`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900">{style.title}</h3>
                  <p className="text-xs text-slate-500">
                    ML Probability Score: <span className="font-semibold text-slate-800">{riskScore}%</span>
                  </p>
                </div>
              </div>
              <button
                onClick={() => setModalOpen(false)}
                className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="mt-5 space-y-4">
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-blue-500" />
                  Primary Driving Factors (Explainable AI)
                </h4>
                <ul className="mt-2 space-y-1.5 text-xs text-slate-700">
                  {contributingFactors && contributingFactors.length > 0 ? (
                    contributingFactors.map((factor, i) => (
                      <li key={i} className="flex items-start gap-2 bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-blue-500 font-bold">•</span>
                        <span>{factor}</span>
                      </li>
                    ))
                  ) : (
                    <li className="text-slate-500 italic">No adverse risk factors identified.</li>
                  )}
                </ul>
              </div>

              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Prescribed Interventions & Next Steps
                </h4>
                <ul className="mt-2 space-y-1.5 text-xs text-slate-700">
                  {recommendations && recommendations.length > 0 ? (
                    recommendations.map((rec, i) => (
                      <li key={i} className="flex items-start gap-2 bg-emerald-50/50 p-2 rounded-lg border border-emerald-100">
                        <span className="text-emerald-600 font-bold">{i + 1}.</span>
                        <span>{rec}</span>
                      </li>
                    ))
                  ) : (
                    <li className="text-slate-500 italic">Maintain your current academic schedule.</li>
                  )}
                </ul>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setModalOpen(false)}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-900 text-white hover:bg-slate-800 transition"
              >
                Close Diagnostics
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
