import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { GraduationCap, Lock, Mail, ArrowRight, ShieldCheck, Sparkles, BookOpen } from 'lucide-react';

export default function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = async (demoEmail, demoPassword) => {
    setEmail(demoEmail);
    setPassword(demoPassword);
    setError('');
    setLoading(true);
    try {
      await login(demoEmail, demoPassword);
    } catch (err) {
      setError(err.response?.data?.detail || 'Demo login failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-slate-50">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="mx-auto w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/20">
          <GraduationCap className="w-8 h-8" />
        </div>
        <h2 className="mt-4 text-3xl font-extrabold text-slate-900 tracking-tight">
          CampusIQ
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          College Academic Intelligence & Student Success Platform
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-6 shadow-xl shadow-slate-200/50 rounded-2xl border border-slate-200 sm:px-10">
          {error && (
            <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-medium">
              {error}
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Email Address
              </label>
              <div className="mt-1.5 relative rounded-xl shadow-2xs">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="student@campusiq.edu"
                  className="block w-full pl-10 pr-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-900"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Password
              </label>
              <div className="mt-1.5 relative rounded-xl shadow-2xs">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="block w-full pl-10 pr-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-900"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center items-center gap-2 py-2.5 px-4 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500/30 shadow-md shadow-blue-500/20 transition disabled:opacity-50"
            >
              {loading ? 'Authenticating...' : 'Sign In to CampusIQ'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Demo Credentials */}
          <div className="mt-6 pt-6 border-t border-slate-100">
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 text-center mb-3">
              Placement Demo 1-Click Access
            </p>
            <div className="grid grid-cols-1 gap-2">
              <button
                type="button"
                onClick={() => handleQuickDemo('kasturi@campusiq.edu', 'Student@123')}
                className="w-full py-2 px-3 text-xs font-medium rounded-xl border border-emerald-200 bg-emerald-50/60 text-emerald-800 hover:bg-emerald-100/70 transition flex items-center justify-between text-left"
              >
                <span>🎓 <strong>Kasturi</strong> (Student - Final Year CSE)</span>
                <span className="text-[10px] font-mono text-emerald-600">8.1 CGPA</span>
              </button>

              <button
                type="button"
                onClick={() => handleQuickDemo('faculty.menon@campusiq.edu', 'Faculty@123')}
                className="w-full py-2 px-3 text-xs font-medium rounded-xl border border-blue-200 bg-blue-50/60 text-blue-800 hover:bg-blue-100/70 transition flex items-center justify-between text-left"
              >
                <span>👨‍🏫 <strong>Prof. Priya Menon</strong> (Faculty - DBMS/OS)</span>
                <span className="text-[10px] font-mono text-blue-600">Assoc. Prof</span>
              </button>

              <button
                type="button"
                onClick={() => handleQuickDemo('admin@campusiq.edu', 'Admin@123')}
                className="w-full py-2 px-3 text-xs font-medium rounded-xl border border-purple-200 bg-purple-50/60 text-purple-800 hover:bg-purple-100/70 transition flex items-center justify-between text-left"
              >
                <span>🏛️ <strong>Dr. K. S. Murthy</strong> (Admin / HOD)</span>
                <span className="text-[10px] font-mono text-purple-600">College-wide</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
