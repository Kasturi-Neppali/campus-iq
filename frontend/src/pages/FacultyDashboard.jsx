import React, { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import StatCard from '../components/StatCard';
import {
  BookOpen, Users, Calendar, AlertTriangle, CheckCircle, Edit3, MessageSquare,
  Search, ShieldAlert, Award, Save
} from 'lucide-react';

export default function FacultyDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [selectedSubjectId, setSelectedSubjectId] = useState(null);
  const [roster, setRoster] = useState(null);
  const [loading, setLoading] = useState(true);
  const [rosterLoading, setRosterLoading] = useState(false);
  const [editRecordId, setEditRecordId] = useState(null);
  const [editMarks, setEditMarks] = useState({ internal: '', assignment: '', final: '' });
  const [editAttendance, setEditAttendance] = useState({ attended: '', total: '' });
  const [remarkModal, setRemarkModal] = useState({ open: false, studentId: null, studentName: '' });
  const [remarkText, setRemarkText] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const fetchFacultyDashboard = async () => {
    try {
      setLoading(true);
      const res = await apiClient.get('/faculty/dashboard');
      setDashboard(res.data);
      if (res.data.subjects && res.data.subjects.length > 0) {
        setSelectedSubjectId(res.data.subjects[0].id);
      }
    } catch (err) {
      console.error('Error fetching faculty dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchRoster = async (subId) => {
    if (!subId) return;
    try {
      setRosterLoading(true);
      const res = await apiClient.get(`/faculty/subject/${subId}/students`);
      setRoster(res.data);
    } catch (err) {
      console.error('Error fetching student roster:', err);
    } finally {
      setRosterLoading(false);
    }
  };

  useEffect(() => {
    fetchFacultyDashboard();
  }, []);

  useEffect(() => {
    if (selectedSubjectId) {
      fetchRoster(selectedSubjectId);
    }
  }, [selectedSubjectId]);

  const handleSaveMarks = async (recordId) => {
    try {
      await apiClient.put(`/faculty/record/${recordId}/marks`, {
        internal_marks: parseFloat(editMarks.internal) || undefined,
        assignment_marks: parseFloat(editMarks.assignment) || undefined,
        final_exam_marks: parseFloat(editMarks.final) || undefined,
      });
      setEditRecordId(null);
      fetchRoster(selectedSubjectId);
    } catch (err) {
      console.error('Failed to update marks:', err);
    }
  };

  const handleSaveAttendance = async (recordId) => {
    try {
      await apiClient.put(`/faculty/record/${recordId}/attendance`, {
        classes_attended: parseInt(editAttendance.attended) || 0,
        total_classes: parseInt(editAttendance.total) || 44,
      });
      setEditRecordId(null);
      fetchRoster(selectedSubjectId);
    } catch (err) {
      console.error('Failed to update attendance:', err);
    }
  };

  const handleSendRemark = async (e) => {
    e.preventDefault();
    if (!remarkText.trim() || !remarkModal.studentId) return;
    try {
      await apiClient.post('/faculty/remarks', {
        student_id: remarkModal.studentId,
        subject_id: selectedSubjectId,
        remark: remarkText,
      });
      setRemarkModal({ open: false, studentId: null, studentName: '' });
      setRemarkText('');
      alert('Remark submitted successfully to student transcript.');
    } catch (err) {
      console.error('Failed to submit remark:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs font-semibold text-slate-500">Loading Faculty Academic Console...</p>
        </div>
      </div>
    );
  }

  const { faculty, stats, subjects } = dashboard || {};
  const filteredStudents = roster?.students?.filter((s) =>
    s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.roll_number.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-blue-900 to-indigo-900 rounded-2xl p-6 text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold">{faculty?.name}</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-white/20 font-medium">
              Emp ID: {faculty?.employee_id}
            </span>
          </div>
          <p className="mt-1 text-xs text-blue-200">
            {faculty?.designation} • {faculty?.department}
          </p>
        </div>

        {/* Subject selector */}
        <div className="flex items-center gap-2 bg-white/10 p-1.5 rounded-xl border border-white/20">
          <BookOpen className="w-4 h-4 text-amber-300 ml-2" />
          <select
            value={selectedSubjectId || ''}
            onChange={(e) => setSelectedSubjectId(parseInt(e.target.value))}
            className="bg-transparent text-white text-xs font-semibold focus:outline-none pr-3 py-1 cursor-pointer"
          >
            {subjects?.map((s) => (
              <option key={s.id} value={s.id} className="text-slate-900">
                {s.name} ({s.code})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Class Average Attendance"
          value={`${stats?.class_average_attendance}%`}
          subtitle="Mandatory university cutoff: 75%"
          icon={Calendar}
          color="blue"
        />
        <StatCard
          title="Class Average Marks"
          value={`${stats?.class_average_internal_marks}%`}
          subtitle="Continuous assessment internal average"
          icon={Award}
          color="indigo"
        />
        <StatCard
          title="Attendance Alerts (<75%)"
          value={stats?.low_attendance_alerts}
          subtitle="Students at risk of exam detention"
          icon={AlertTriangle}
          color="amber"
        />
        <StatCard
          title="Academic Risk Students"
          value={stats?.at_risk_students_count}
          subtitle="Identified by ML Early Intervention"
          icon={ShieldAlert}
          color="rose"
        />
      </div>

      {/* Student Roster Section */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900">
              Student Class Roster & Evaluation Management
            </h3>
            <p className="text-xs text-slate-500">
              {roster?.subject?.name} ({roster?.subject?.code}) • {roster?.students?.length || 0} enrolled students
            </p>
          </div>

          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Filter by student name or roll..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-3.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 w-64 text-slate-800"
            />
          </div>
        </div>

        {rosterLoading ? (
          <div className="p-12 text-center text-xs text-slate-500 animate-pulse">
            Loading student rosters and risk classifications...
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Student Details</th>
                  <th className="py-3 px-4">Attendance</th>
                  <th className="py-3 px-4">Internal (50)</th>
                  <th className="py-3 px-4">Assignments (25)</th>
                  <th className="py-3 px-4">Final (100)</th>
                  <th className="py-3 px-4">Risk Tag</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {filteredStudents?.map((stu) => {
                  const isEditing = editRecordId === stu.record_id;
                  return (
                    <tr key={stu.record_id} className="hover:bg-slate-50/80 transition">
                      <td className="py-3 px-4">
                        <div className="font-semibold text-slate-900">{stu.name}</div>
                        <div className="text-[11px] text-slate-400 font-mono">
                          {stu.roll_number} • CGPA: {stu.cgpa} • Backlogs: {stu.backlogs}
                        </div>
                      </td>

                      <td className="py-3 px-4">
                        {isEditing ? (
                          <div className="flex items-center gap-1">
                            <input
                              type="number"
                              className="w-12 px-1 py-0.5 border border-slate-300 rounded text-center text-xs"
                              defaultValue={stu.classes_attended}
                              onChange={(e) =>
                                setEditAttendance({ ...editAttendance, attended: e.target.value })
                              }
                            />
                            <span>/</span>
                            <input
                              type="number"
                              className="w-12 px-1 py-0.5 border border-slate-300 rounded text-center text-xs"
                              defaultValue={stu.total_classes}
                              onChange={(e) =>
                                setEditAttendance({ ...editAttendance, total: e.target.value })
                              }
                            />
                            <button
                              onClick={() => handleSaveAttendance(stu.record_id)}
                              className="p-1 bg-emerald-600 text-white rounded hover:bg-emerald-700"
                              title="Save Attendance"
                            >
                              <Save className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ) : (
                          <div className="flex items-center gap-1.5">
                            <span
                              className={`font-semibold ${
                                stu.attendance_percentage < 75 ? 'text-rose-600 font-bold' : 'text-slate-900'
                              }`}
                            >
                              {stu.attendance_percentage}%
                            </span>
                            <span className="text-[11px] text-slate-400">
                              ({stu.classes_attended}/{stu.total_classes})
                            </span>
                          </div>
                        )}
                      </td>

                      <td className="py-3 px-4">
                        {isEditing ? (
                          <input
                            type="number"
                            step="0.5"
                            className="w-16 px-1.5 py-0.5 border border-slate-300 rounded text-xs text-center"
                            defaultValue={stu.internal_marks}
                            onChange={(e) =>
                              setEditMarks({ ...editMarks, internal: e.target.value })
                            }
                          />
                        ) : (
                          <span className="font-semibold text-slate-900">{stu.internal_marks}</span>
                        )}
                      </td>

                      <td className="py-3 px-4">
                        {isEditing ? (
                          <input
                            type="number"
                            step="0.5"
                            className="w-16 px-1.5 py-0.5 border border-slate-300 rounded text-xs text-center"
                            defaultValue={stu.assignment_marks}
                            onChange={(e) =>
                              setEditMarks({ ...editMarks, assignment: e.target.value })
                            }
                          />
                        ) : (
                          <span className="font-semibold text-slate-900">{stu.assignment_marks}</span>
                        )}
                      </td>

                      <td className="py-3 px-4">
                        {isEditing ? (
                          <div className="flex items-center gap-1">
                            <input
                              type="number"
                              className="w-16 px-1.5 py-0.5 border border-slate-300 rounded text-xs text-center"
                              defaultValue={stu.final_exam_marks}
                              onChange={(e) =>
                                setEditMarks({ ...editMarks, final: e.target.value })
                              }
                            />
                            <button
                              onClick={() => handleSaveMarks(stu.record_id)}
                              className="p-1 bg-blue-600 text-white rounded hover:bg-blue-700"
                              title="Save Marks"
                            >
                              <Save className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ) : (
                          <span className="font-semibold text-slate-900">{stu.final_exam_marks}</span>
                        )}
                      </td>

                      <td className="py-3 px-4">
                        <span
                          className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            stu.risk_tag === 'HIGH'
                              ? 'bg-rose-100 text-rose-700'
                              : stu.risk_tag === 'MEDIUM'
                              ? 'bg-amber-100 text-amber-700'
                              : 'bg-emerald-100 text-emerald-700'
                          }`}
                        >
                          {stu.risk_tag} RISK
                        </span>
                      </td>

                      <td className="py-3 px-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => {
                              if (isEditing) {
                                setEditRecordId(null);
                              } else {
                                setEditRecordId(stu.record_id);
                                setEditMarks({
                                  internal: stu.internal_marks,
                                  assignment: stu.assignment_marks,
                                  final: stu.final_exam_marks,
                                });
                                setEditAttendance({
                                  attended: stu.classes_attended,
                                  total: stu.total_classes,
                                });
                              }
                            }}
                            className="p-1 text-slate-400 hover:text-blue-600 transition"
                            title="Edit marks & attendance"
                          >
                            <Edit3 className="w-4 h-4" />
                          </button>

                          <button
                            onClick={() =>
                              setRemarkModal({
                                open: true,
                                studentId: stu.student_id,
                                studentName: stu.name,
                              })
                            }
                            className="p-1 text-slate-400 hover:text-indigo-600 transition"
                            title="Add mentor remark"
                          >
                            <MessageSquare className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Remark Modal */}
      {remarkModal.open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200">
            <h3 className="text-sm font-bold text-slate-900">
              Submit Academic Remark for {remarkModal.studentName}
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              This remark will appear in the student's personal dashboard and CampusAI context.
            </p>
            <form onSubmit={handleSendRemark} className="mt-4 space-y-3">
              <textarea
                rows="3"
                required
                value={remarkText}
                onChange={(e) => setRemarkText(e.target.value)}
                placeholder="Enter targeted guidance or remedial recommendation..."
                className="w-full p-3 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20"
              />
              <div className="flex justify-end gap-2 text-xs font-semibold">
                <button
                  type="button"
                  onClick={() => setRemarkModal({ open: false, studentId: null, studentName: '' })}
                  className="px-3 py-2 text-slate-600 hover:bg-slate-100 rounded-lg transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  Post Remark
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
