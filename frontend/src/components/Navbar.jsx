import React from 'react';
import { useAuth } from '../context/AuthContext';
import { GraduationCap, LogOut, User, Sparkles, Shield, BookOpen, Building2 } from 'lucide-react';

export default function Navbar({ onOpenAI }) {
  const { user, logout, login } = useAuth();

  const handleQuickSwitch = async (roleType) => {
    try {
      if (roleType === 'student') {
        await login('kasturi@campusiq.edu', 'Student@123');
      } else if (roleType === 'faculty') {
        await login('faculty.menon@campusiq.edu', 'Faculty@123');
      } else if (roleType === 'admin') {
        await login('admin@campusiq.edu', 'Admin@123');
      }
    } catch (err) {
      console.error('Failed to switch user:', err);
    }
  };

  const getRoleBadge = (role) => {
    switch (role) {
      case 'admin':
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-200"><Shield className="w-3 h-3" /> Admin / HOD</span>;
      case 'faculty':
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-200"><BookOpen className="w-3 h-3" /> Faculty</span>;
      case 'student':
      default:
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200"><GraduationCap className="w-3 h-3" /> Student</span>;
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-slate-900 via-blue-950 to-indigo-900 bg-clip-text text-transparent">
                CampusIQ
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 bg-blue-50 text-blue-700 rounded border border-blue-200">
                v1.0 AI
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">Academic Intelligence & Student Success Platform</p>
          </div>
        </div>

        {/* Quick Demo Switcher & Controls */}
        <div className="flex items-center gap-3">
          {/* Quick Switch for Placement Demo */}
          <div className="hidden md:flex items-center gap-1 bg-slate-100 p-1 rounded-lg text-xs border border-slate-200">
            <span className="text-slate-400 font-medium px-2 text-[11px]">Demo Role:</span>
            <button
              onClick={() => handleQuickSwitch('student')}
              className={`px-2.5 py-1 rounded font-medium transition ${user?.role === 'student' ? 'bg-white text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
            >
              🎓 Student
            </button>
            <button
              onClick={() => handleQuickSwitch('faculty')}
              className={`px-2.5 py-1 rounded font-medium transition ${user?.role === 'faculty' ? 'bg-white text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
            >
              👨‍🏫 Faculty
            </button>
            <button
              onClick={() => handleQuickSwitch('admin')}
              className={`px-2.5 py-1 rounded font-medium transition ${user?.role === 'admin' ? 'bg-white text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
            >
              🏛️ HOD / Admin
            </button>
          </div>

          {/* AI Assistant button */}
          <button
            onClick={onOpenAI}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-gradient-to-r from-indigo-600 to-blue-600 text-white shadow-sm hover:from-indigo-700 hover:to-blue-700 transition"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span className="hidden sm:inline">Ask</span> CampusAI
          </button>

          {/* User profile & Logout */}
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
            <div className="hidden lg:block text-right">
              <div className="text-xs font-semibold text-slate-800 leading-tight">{user?.name}</div>
              <div className="mt-0.5">{getRoleBadge(user?.role)}</div>
            </div>
            <button
              onClick={logout}
              title="Logout"
              className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
