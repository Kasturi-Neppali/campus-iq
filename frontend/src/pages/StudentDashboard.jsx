import React, { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import StatCard from '../components/StatCard';
import RiskBadge from '../components/RiskBadge';
import {
  GraduationCap, BookOpen, AlertTriangle, TrendingUp, Sparkles, CheckCircle2,
  Briefcase, Code, Award, Sliders, Calendar, ArrowUpRight, Plus, Trash2, Shield
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';

import AcademicOnboardingModal from '../components/AcademicOnboardingModal';

export default function StudentDashboard({ onOpenAI }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('academics'); // academics, whatif, placement, portfolio, remarks

  // What-If Simulator state
  const [targetCgpa, setTargetCgpa] = useState(8.5);
  const [expectedMarks, setExpectedMarks] = useState({});
  const [addlAttended, setAddlAttended] = useState(12);
  const [addlTotal, setAddlTotal] = useState(14);
  const [simResult, setSimResult] = useState(null);
  const [simLoading, setSimLoading] = useState(false);

  // Portfolio add state
  const [newSkill, setNewSkill] = useState('');
  const [newSkillProf, setNewSkillProf] = useState('Intermediate');
  const [newProjTitle, setNewProjTitle] = useState('');
  const [newProjTech, setNewProjTech] = useState('');
  const [newProjDesc, setNewProjDesc] = useState('');
  
  const [isOnboardingOpen, setIsOnboardingOpen] = useState(false);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const res = await apiClient.get('/student/dashboard');
      setData(res.data);
      
      // Auto-open onboarding if no subjects exist yet (which means attendance is 0 and no data)
      if (res.data.subjects?.length === 0) {
        setIsOnboardingOpen(true);
      }

      // Initialize what-if marks
      const marksMap = {};
      res.data.subjects?.forEach((s) => {
        marksMap[s.subject_id] = s.final_exam_marks || 75;
      });
      setExpectedMarks(marksMap);
    } catch (err) {
      console.error('Error fetching dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleSimulate = async () => {
    setSimLoading(true);
    try {
      const payloadExpected = Object.entries(expectedMarks).map(([subId, marks]) => ({
        subject_id: parseInt(subId),
        subject_name: data?.subjects?.find((s) => s.subject_id === parseInt(subId))?.name || 'Subject',
        expected_marks: parseFloat(marks),
      }));

      const res = await apiClient.post('/simulator/simulate', {
        target_cgpa: parseFloat(targetCgpa) || null,
        expected_subject_marks: payloadExpected,
        additional_classes_to_attend: parseInt(addlAttended) || 0,
        total_additional_classes: parseInt(addlTotal) || 0,
      });
      setSimResult(res.data);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setSimLoading(false);
    }
  };

  const handleAddSkill = async (e) => {
    e.preventDefault();
    if (!newSkill.trim()) return;
    try {
      await apiClient.post('/student/skills', { skill_name: newSkill, proficiency: newSkillProf });
      setNewSkill('');
      fetchDashboard();
    } catch (err) {
      console.error('Failed to add skill:', err);
    }
  };

  const handleDeleteSkill = async (id) => {
    try {
      await apiClient.delete(`/student/skills/${id}`);
      fetchDashboard();
    } catch (err) {
      console.error('Failed to delete skill:', err);
    }
  };

  const handleAddProject = async (e) => {
    e.preventDefault();
    if (!newProjTitle.trim()) return;
    try {
      await apiClient.post('/student/projects', {
        title: newProjTitle,
        tech_stack: newProjTech,
        description: newProjDesc,
      });
      setNewProjTitle('');
      setNewProjTech('');
      setNewProjDesc('');
      fetchDashboard();
    } catch (err) {
      console.error('Failed to add project:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs font-semibold text-slate-500">Loading Academic Intelligence Hub...</p>
        </div>
      </div>
    );
  }

  const { student, stats, subjects, weak_subjects, risk_details, placement_details, portfolio } = data || {};

  // Chart data for subject performance
  const subjectChartData = subjects?.map((s) => ({
    name: s.code,
    fullName: s.name,
    Internal: s.internal_percentage,
    Attendance: s.attendance_percentage,
    Final: s.final_exam_marks,
  })) || [];

  // Placement radar chart data
  const placementRadarData = [
    { subject: 'DSA', score: placement_details?.dsa_score || 70, fullMark: 100 },
    { subject: 'Programming', score: placement_details?.programming_score || 80, fullMark: 100 },
    { subject: 'Aptitude', score: placement_details?.aptitude_score || 65, fullMark: 100 },
    { subject: 'Communication', score: placement_details?.communication_score || 75, fullMark: 100 },
    { subject: 'Projects', score: placement_details?.projects_score || 90, fullMark: 100 },
    { subject: 'Certifications', score: placement_details?.certifications_score || 70, fullMark: 100 },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <AcademicOnboardingModal 
        isOpen={isOnboardingOpen}
        onClose={() => setIsOnboardingOpen(false)}
        onSave={fetchDashboard}
        defaultData={data?.stats}
      />
      {/* Student Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-indigo-950 rounded-2xl p-6 text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6 border border-slate-800">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-extrabold tracking-tight">{student?.name}</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 font-medium">
              Roll: {student?.roll_number}
            </span>
          </div>
          <p className="mt-1 text-xs text-blue-200">
            {student?.department} • Year {student?.year}, Semester {student?.semester} (Sec {student?.section})
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={() => setIsOnboardingOpen(true)}
            className="text-xs px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg transition"
          >
            Update Info
          </button>
          <RiskBadge
            riskLevel={stats?.risk_level}
            riskScore={stats?.risk_score}
            contributingFactors={risk_details?.contributing_factors}
            recommendations={risk_details?.recommendations}
          />

          <button
            onClick={onOpenAI}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-md shadow-blue-600/30 transition"
          >
            <Sparkles className="w-4 h-4 text-amber-300" />
            Ask CampusAI
          </button>
        </div>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Cumulative CGPA"
          value={stats?.cgpa?.toFixed(2)}
          subtitle="Out of 10.0 scale"
          icon={GraduationCap}
          color="blue"
        />
        <StatCard
          title="Overall Attendance"
          value={`${stats?.attendance_pct}%`}
          subtitle={stats?.attendance_pct >= 75 ? 'Above 75% cutoff' : 'Detention Risk Warning'}
          icon={Calendar}
          color={stats?.attendance_pct >= 75 ? 'emerald' : 'rose'}
        />
        <StatCard
          title="Active Backlogs"
          value={stats?.backlogs}
          subtitle={stats?.backlogs === 0 ? 'Clear academic record' : 'Requires supplementary'}
          icon={AlertTriangle}
          color={stats?.backlogs === 0 ? 'emerald' : 'rose'}
        />
        <StatCard
          title="Academic Risk"
          value={stats?.risk_level}
          subtitle={`Probability score: ${stats?.risk_score}%`}
          icon={Shield}
          color={stats?.risk_level === 'LOW' ? 'emerald' : stats?.risk_level === 'MEDIUM' ? 'amber' : 'rose'}
        />
        <StatCard
          title="Placement Readiness"
          value={`${stats?.placement_readiness}%`}
          subtitle={placement_details?.readiness_tier}
          icon={Briefcase}
          color="indigo"
        />
      </div>

      {/* Weak Subjects Diagnostic Banner (if any) */}
      {weak_subjects && weak_subjects.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="text-xs">
            <span className="font-bold text-amber-900">Attention Needed: </span>
            <span className="text-amber-800">
              The academic intelligence engine detected lower internal performance or attendance in:{' '}
              <strong>{weak_subjects.map((w) => `${w.name} (${w.code})`).join(', ')}</strong>.
            </span>
            <div className="mt-1 text-amber-700">
              Prescription: Attend remaining lecture hours and review faculty doubt-clearing sessions to build exam buffer.
            </div>
          </div>
        </div>
      )}

      {/* Tabs Navigation */}
      <div className="flex border-b border-slate-200 gap-6 text-xs font-semibold">
        <button
          onClick={() => setActiveTab('academics')}
          className={`pb-3 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === 'academics'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <BookOpen className="w-4 h-4" /> Academic Performance
        </button>
        <button
          onClick={() => setActiveTab('whatif')}
          className={`pb-3 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === 'whatif'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Sliders className="w-4 h-4" /> What-If Simulator
        </button>
        <button
          onClick={() => setActiveTab('placement')}
          className={`pb-3 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === 'placement'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Briefcase className="w-4 h-4" /> Placement Readiness
        </button>
        <button
          onClick={() => setActiveTab('portfolio')}
          className={`pb-3 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === 'portfolio'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Code className="w-4 h-4" /> Skills & Projects
        </button>
      </div>

      {/* TAB 1: ACADEMICS */}
      {activeTab === 'academics' && (
        <div className="space-y-6">
          {/* Performance Chart */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-4">Subject-Wise Analytics (Marks vs Attendance)</h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={subjectChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#fff', borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }}
                  />
                  <Bar dataKey="Attendance" fill="#0c85eb" radius={[4, 4, 0, 0]} name="Attendance %" />
                  <Bar dataKey="Internal" fill="#6366f1" radius={[4, 4, 0, 0]} name="Internal Marks %" />
                  <Bar dataKey="Final" fill="#10b981" radius={[4, 4, 0, 0]} name="Final Exam Score" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Subjects Table */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="p-4 border-b border-slate-100 flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-900">Enrolled Subjects & Evaluations</h3>
              <span className="text-xs text-slate-500">Semester {student?.semester} Curriculum</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-b border-slate-200">
                  <tr>
                    <th className="py-3 px-4">Subject Code & Name</th>
                    <th className="py-3 px-4">Credits</th>
                    <th className="py-3 px-4">Attendance</th>
                    <th className="py-3 px-4">Internal Marks</th>
                    <th className="py-3 px-4">Assignments</th>
                    <th className="py-3 px-4">Final Marks</th>
                    <th className="py-3 px-4">Grade</th>
                    <th className="py-3 px-4">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-slate-700">
                  {subjects?.map((s) => (
                    <tr key={s.record_id} className="hover:bg-slate-50/80 transition">
                      <td className="py-3 px-4">
                        <div className="font-semibold text-slate-900">{s.name}</div>
                        <div className="text-[11px] text-slate-400 font-mono">{s.code}</div>
                      </td>
                      <td className="py-3 px-4 font-medium">{s.credits}</td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <span className={`font-semibold ${s.attendance_percentage < 75 ? 'text-rose-600' : 'text-slate-900'}`}>
                            {s.attendance_percentage}%
                          </span>
                          <span className="text-[11px] text-slate-400">({s.classes_attended}/{s.total_classes})</span>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className="font-semibold text-slate-900">{s.internal_marks}</span>
                        <span className="text-[11px] text-slate-400"> / 50 ({s.internal_percentage}%)</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="font-semibold text-slate-900">{s.assignment_marks}</span>
                        <span className="text-[11px] text-slate-400"> / 25</span>
                      </td>
                      <td className="py-3 px-4 font-semibold text-slate-900">
                        {s.final_exam_marks} / 100
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded font-bold bg-slate-100 text-slate-800">
                          {s.grade}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            s.status === 'Critical'
                              ? 'bg-rose-100 text-rose-700'
                              : s.status === 'Average'
                              ? 'bg-amber-100 text-amber-700'
                              : 'bg-emerald-100 text-emerald-700'
                          }`}
                        >
                          {s.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: WHAT-IF SIMULATOR */}
      {activeTab === 'whatif' && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
            <div className="max-w-2xl">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Sliders className="w-5 h-5 text-blue-600" />
                Academic What-If Simulator & Goal Solver
              </h3>
              <p className="mt-1 text-xs text-slate-500">
                Model hypothetical exam marks and attendance scenarios to project your resulting SGPA and cumulative CGPA.
              </p>
            </div>

            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Expected Subject Marks */}
              <div className="space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Simulate Expected Subject Marks (out of 100)
                </h4>
                <div className="space-y-3">
                  {subjects?.map((s) => (
                    <div key={s.subject_id} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                      <div>
                        <div className="font-semibold text-slate-900">{s.name}</div>
                        <div className="text-[11px] text-slate-400 font-mono">{s.code} ({s.credits} Credits)</div>
                      </div>
                      <div className="flex items-center gap-2">
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={expectedMarks[s.subject_id] || ''}
                          onChange={(e) =>
                            setExpectedMarks({ ...expectedMarks, [s.subject_id]: e.target.value })
                          }
                          className="w-16 px-2 py-1 bg-white border border-slate-300 rounded-lg text-center font-bold text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                        />
                        <span className="text-slate-400">/ 100</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Target & Attendance Solver */}
              <div className="space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Target CGPA & Attendance Goals
                </h4>
                <div className="p-4 rounded-xl bg-blue-50/50 border border-blue-100 space-y-3 text-xs">
                  <div>
                    <label className="block font-semibold text-blue-950 mb-1">Target Cumulative CGPA</label>
                    <input
                      type="number"
                      step="0.05"
                      min="5.0"
                      max="10.0"
                      value={targetCgpa}
                      onChange={(e) => setTargetCgpa(e.target.value)}
                      className="w-full px-3 py-1.5 bg-white border border-blue-200 rounded-lg font-bold text-blue-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                    />
                  </div>

                  <div className="pt-2 border-t border-blue-100 grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-[11px] text-slate-600 mb-1">Classes to Attend</label>
                      <input
                        type="number"
                        min="0"
                        value={addlAttended}
                        onChange={(e) => setAddlAttended(e.target.value)}
                        className="w-full px-2 py-1 bg-white border border-slate-300 rounded-lg font-semibold text-slate-900"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] text-slate-600 mb-1">Out of Upcoming Classes</label>
                      <input
                        type="number"
                        min="1"
                        value={addlTotal}
                        onChange={(e) => setAddlTotal(e.target.value)}
                        className="w-full px-2 py-1 bg-white border border-slate-300 rounded-lg font-semibold text-slate-900"
                      />
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleSimulate}
                  disabled={simLoading}
                  className="w-full py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md shadow-blue-500/20 transition disabled:opacity-50"
                >
                  {simLoading ? 'Simulating Trajectory...' : 'Run Simulation & Goal Solver'}
                </button>

                {/* Simulation Output Card */}
                {simResult && (
                  <div className="p-4 rounded-xl bg-slate-900 text-white space-y-3 animate-in fade-in duration-150">
                    <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                      <span className="text-xs text-slate-400 font-medium">Projected Semester SGPA</span>
                      <span className="text-lg font-bold text-emerald-400">{simResult.projected_sgpa || '—'}</span>
                    </div>
                    <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                      <span className="text-xs text-slate-400 font-medium">New Projected CGPA</span>
                      <span className="text-lg font-bold text-blue-400">{simResult.projected_cgpa || '—'}</span>
                    </div>
                    {simResult.projected_attendance_pct && (
                      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                        <span className="text-xs text-slate-400 font-medium">Projected Attendance</span>
                        <span className="text-sm font-bold text-amber-300">{simResult.projected_attendance_pct}%</span>
                      </div>
                    )}
                    <div className="text-xs text-slate-300 pt-1 leading-relaxed bg-slate-800/60 p-2.5 rounded-lg border border-slate-700">
                      <strong>Goal Solver Verdict: </strong> {simResult.feasibility_message}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: PLACEMENT READINESS */}
      {activeTab === 'placement' && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-100">
              <div>
                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Briefcase className="w-5 h-5 text-indigo-600" />
                  Placement Preparation & Skill Readiness
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Multifactorial evaluation comparing DSA, Core Coding, Aptitude, Projects, and Soft Skills.
                </p>
              </div>
              <div className="bg-indigo-50 border border-indigo-100 px-4 py-2 rounded-xl text-right">
                <div className="text-[11px] text-indigo-600 font-semibold uppercase">Overall Readiness</div>
                <div className="text-2xl font-black text-indigo-950">{placement_details?.overall_readiness}%</div>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              {/* Radar Chart */}
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={placementRadarData}>
                    <PolarGrid stroke="#e2e8f0" />
                    <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11, fill: '#475569' }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 10 }} />
                    <Radar name="Student Score" dataKey="score" stroke="#4f46e5" fill="#6366f1" fillOpacity={0.4} />
                    <Tooltip contentStyle={{ borderRadius: '12px', fontSize: '12px' }} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              {/* Breakdown List & Areas to Improve */}
              <div className="space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Priority Areas to Improve (Deficit Diagnostics)
                </h4>
                <div className="space-y-2">
                  {placement_details?.areas_to_improve?.map((area, i) => (
                    <div key={i} className="flex items-start gap-2.5 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                      <span className="p-1 rounded-full bg-indigo-100 text-indigo-600 font-bold shrink-0">
                        {i + 1}
                      </span>
                      <span className="text-slate-800 font-medium leading-relaxed">{area}</span>
                    </div>
                  ))}
                </div>

                <div className="p-3 rounded-xl bg-amber-50/70 border border-amber-200 text-[11px] text-amber-800 leading-relaxed">
                  <strong>Institutional Notice: </strong> {placement_details?.disclaimer}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: PORTFOLIO & SKILLS */}
      {activeTab === 'portfolio' && (
        <div className="space-y-6">
          {/* Skills Grid */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Code className="w-4 h-4 text-blue-600" /> Verified Technical Skills
              </h3>
            </div>

            <div className="flex flex-wrap gap-2 mb-6">
              {portfolio?.skills?.map((sk) => (
                <div
                  key={sk.id}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-800 group"
                >
                  <span>{sk.skill_name}</span>
                  <span className="text-[10px] text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-100">
                    {sk.proficiency}
                  </span>
                  <button
                    onClick={() => handleDeleteSkill(sk.id)}
                    className="text-slate-400 hover:text-rose-600 transition"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>

            <form onSubmit={handleAddSkill} className="flex items-center gap-3 pt-4 border-t border-slate-100 text-xs">
              <input
                type="text"
                placeholder="Add new skill (e.g. Docker, TypeScript)..."
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                className="flex-1 px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20"
              />
              <select
                value={newSkillProf}
                onChange={(e) => setNewSkillProf(e.target.value)}
                className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-slate-700"
              >
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition"
              >
                Add Skill
              </button>
            </form>
          </div>

          {/* Projects Showcase */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
              <Award className="w-4 h-4 text-emerald-600" /> Featured Engineering Projects
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {portfolio?.projects?.map((p) => (
                <div key={p.id} className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-2">
                  <div className="font-bold text-slate-900 text-sm">{p.title}</div>
                  <p className="text-slate-600 leading-relaxed">{p.description}</p>
                  <div className="text-[11px] font-mono text-blue-700 font-medium">Stack: {p.tech_stack}</div>
                </div>
              ))}
            </div>

            <form onSubmit={handleAddProject} className="space-y-3 pt-4 border-t border-slate-100 text-xs">
              <div className="font-semibold text-slate-800">Add New Placement Project</div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <input
                  type="text"
                  placeholder="Project Title..."
                  value={newProjTitle}
                  onChange={(e) => setNewProjTitle(e.target.value)}
                  className="px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                />
                <input
                  type="text"
                  placeholder="Tech Stack (e.g. React, Python, PostgreSQL)..."
                  value={newProjTech}
                  onChange={(e) => setNewProjTech(e.target.value)}
                  className="px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
              <textarea
                rows="2"
                placeholder="Brief project impact & problem statement..."
                value={newProjDesc}
                onChange={(e) => setNewProjDesc(e.target.value)}
                className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition"
              >
                Save Project
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
