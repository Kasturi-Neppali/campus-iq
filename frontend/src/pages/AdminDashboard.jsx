import React, { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import StatCard from '../components/StatCard';
import {
  Building2, Users, GraduationCap, ShieldAlert, Award, Calendar, Search, Filter
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  PieChart, Pie, Cell, Legend
} from 'recharts';

export default function AdminDashboard() {
  const [overview, setOverview] = useState(null);
  const [departments, setDepartments] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterRisk, setFilterRisk] = useState('ALL');

  const fetchAdminData = async () => {
    try {
      setLoading(true);
      const [ovRes, deptRes, stuRes] = await Promise.all([
        apiClient.get('/admin/overview'),
        apiClient.get('/admin/departments'),
        apiClient.get('/admin/students'),
      ]);
      setOverview(ovRes.data);
      setDepartments(deptRes.data);
      setStudents(stuRes.data);
    } catch (err) {
      console.error('Failed to fetch admin statistics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-purple-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs font-semibold text-slate-500">Compiling Institutional Intelligence...</p>
        </div>
      </div>
    );
  }

  // Risk Pie Data
  const riskPieData = [
    { name: 'Low Risk', value: overview?.risk_breakdown?.low || 0, color: '#10b981' },
    { name: 'Medium Risk', value: overview?.risk_breakdown?.medium || 0, color: '#f59e0b' },
    { name: 'High Risk', value: overview?.risk_breakdown?.high || 0, color: '#f43f5e' },
  ];

  const filteredStudents = students.filter((s) => {
    const matchesSearch =
      s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.roll_number.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesRisk = filterRisk === 'ALL' || s.risk_level === filterRisk;
    return matchesSearch && matchesRisk;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-purple-950 to-indigo-950 rounded-2xl p-6 text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4 border border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold">Executive Academic Console</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-400/30 font-medium">
              Dean & HOD Portal
            </span>
          </div>
          <p className="mt-1 text-xs text-purple-200">
            College-Wide Academic Trajectories, Retention Analytics & Placement Indicators
          </p>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Total Students"
          value={overview?.total_students}
          subtitle="Enrolled undergraduates"
          icon={Users}
          color="blue"
        />
        <StatCard
          title="Faculty Members"
          value={overview?.total_faculty}
          subtitle="Across all departments"
          icon={Building2}
          color="indigo"
        />
        <StatCard
          title="Institutional CGPA"
          value={overview?.average_cgpa?.toFixed(2)}
          subtitle="College cumulative mean"
          icon={GraduationCap}
          color="purple"
        />
        <StatCard
          title="College Attendance"
          value={`${overview?.college_attendance_average}%`}
          subtitle="Institutional average"
          icon={Calendar}
          color="emerald"
        />
        <StatCard
          title="Avg Placement Readiness"
          value={`${overview?.average_placement_readiness}%`}
          subtitle="Cohort benchmark score"
          icon={Award}
          color="amber"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution Pie */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 mb-2">Student Academic Risk Distribution</h3>
          <p className="text-xs text-slate-500 mb-4">ML Early Intervention classification</p>
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={riskPieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {riskPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend verticalAlign="bottom" height={36} iconSize={8} wrapperStyle={{ fontSize: '11px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Department Comparison Bar */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs lg:col-span-2">
          <h3 className="text-sm font-bold text-slate-900 mb-2">Departmental Academic Performance</h3>
          <p className="text-xs text-slate-500 mb-4">Average CGPA and Backlogs across engineering departments</p>
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={departments} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="department" tick={{ fontSize: 10 }} />
                <YAxis domain={[0, 10]} tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ borderRadius: '12px', fontSize: '12px' }} />
                <Bar dataKey="average_cgpa" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Average CGPA" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* College Students Directory */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Institutional Student Directory</h3>
            <p className="text-xs text-slate-500">Live monitoring of academic metrics & risk flags</p>
          </div>

          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="Search student or roll..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 pr-3.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500/20 text-slate-800"
              />
            </div>

            <select
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
              className="py-1.5 px-3 text-xs bg-slate-50 border border-slate-200 rounded-xl font-medium text-slate-700"
            >
              <option value="ALL">All Risk Levels</option>
              <option value="LOW">Low Risk Only</option>
              <option value="MEDIUM">Medium Risk Only</option>
              <option value="HIGH">High Risk Only</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Student</th>
                <th className="py-3 px-4">Department & Year</th>
                <th className="py-3 px-4">CGPA</th>
                <th className="py-3 px-4">Attendance</th>
                <th className="py-3 px-4">Backlogs</th>
                <th className="py-3 px-4">Placement Readiness</th>
                <th className="py-3 px-4">Risk Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {filteredStudents.map((stu) => (
                <tr key={stu.id} className="hover:bg-slate-50/80 transition">
                  <td className="py-3 px-4">
                    <div className="font-semibold text-slate-900">{stu.name}</div>
                    <div className="text-[11px] text-slate-400 font-mono">{stu.roll_number}</div>
                  </td>
                  <td className="py-3 px-4">
                    <div>{stu.department}</div>
                    <div className="text-[11px] text-slate-400">Year {stu.year}, Sem {stu.semester} ({stu.section})</div>
                  </td>
                  <td className="py-3 px-4 font-bold text-slate-900">{stu.cgpa.toFixed(2)}</td>
                  <td className="py-3 px-4">
                    <span className={`font-semibold ${stu.attendance_percentage < 75 ? 'text-rose-600 font-bold' : 'text-slate-800'}`}>
                      {stu.attendance_percentage}%
                    </span>
                  </td>
                  <td className="py-3 px-4 font-medium">{stu.backlogs}</td>
                  <td className="py-3 px-4">
                    <span className="font-semibold text-indigo-700">{stu.placement_readiness}%</span>
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        stu.risk_level === 'HIGH'
                          ? 'bg-rose-100 text-rose-700'
                          : stu.risk_level === 'MEDIUM'
                          ? 'bg-amber-100 text-amber-700'
                          : 'bg-emerald-100 text-emerald-700'
                      }`}
                    >
                      {stu.risk_level} RISK
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
