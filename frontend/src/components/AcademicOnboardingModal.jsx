import React, { useState, useEffect } from 'react';
import { GraduationCap, Trash2, Plus, ArrowRight, ArrowLeft } from 'lucide-react';
import apiClient from '../api/apiClient';

export default function AcademicOnboardingModal({ isOpen, onClose, onSave, defaultData }) {
  const [step, setStep] = useState(1);
  const [cgpa, setCgpa] = useState(defaultData?.cgpa || '');
  const [attendance, setAttendance] = useState(defaultData?.attendance_pct || '');
  const [backlogs, setBacklogs] = useState(defaultData?.backlogs || '0');
  
  const [subjects, setSubjects] = useState([
    { subject_code: '', subject_name: '', credits: 3, classes_attended: 0, total_classes: 40, internal_marks: 0, assignment_marks: 0, final_exam_marks: 0 }
  ]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setCgpa(defaultData?.cgpa || '');
      setAttendance(defaultData?.attendance_pct || '');
      setBacklogs(defaultData?.backlogs?.toString() || '0');
      setStep(1);
      // We could also populate subjects if they already have them, but for onboarding we can start fresh or empty.
    }
  }, [isOpen, defaultData]);

  if (!isOpen) return null;

  const handleAddSubject = () => {
    setSubjects([...subjects, { subject_code: '', subject_name: '', credits: 3, classes_attended: 0, total_classes: 40, internal_marks: 0, assignment_marks: 0, final_exam_marks: 0 }]);
  };

  const handleRemoveSubject = (index) => {
    setSubjects(subjects.filter((_, i) => i !== index));
  };

  const handleSubjectChange = (index, field, value) => {
    const newSubjects = [...subjects];
    // parse numeric fields
    if (['credits', 'classes_attended', 'total_classes'].includes(field)) {
      newSubjects[index][field] = parseInt(value) || 0;
    } else if (['internal_marks', 'assignment_marks', 'final_exam_marks'].includes(field)) {
      newSubjects[index][field] = parseFloat(value) || 0;
    } else {
      newSubjects[index][field] = value;
    }
    setSubjects(newSubjects);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // only send subjects that have a code
      const validSubjects = subjects.filter(s => s.subject_code.trim() !== '');
      
      await apiClient.post('/student/update_academic_profile', {
        cgpa: parseFloat(cgpa) || 0,
        attendance_pct: parseFloat(attendance) || 0,
        backlogs: parseInt(backlogs) || 0,
        subjects: validSubjects.length > 0 ? validSubjects : null
      });
      await onSave();
      onClose();
    } catch (err) {
      console.error('Failed to update profile:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div className={`bg-white rounded-2xl shadow-2xl w-full ${step === 1 ? 'max-w-md' : 'max-w-4xl'} overflow-hidden transition-all duration-300 max-h-[90vh] flex flex-col`}>
        <div className="bg-blue-600 p-6 text-white text-center shrink-0">
          <GraduationCap className="w-10 h-10 mx-auto mb-2 opacity-90" />
          <h2 className="text-xl font-bold">Academic Profile Setup</h2>
          <p className="text-blue-100 text-xs mt-1">
            {step === 1 ? 'Step 1: General Academic Overview' : 'Step 2: Enrolled Subjects & Evaluations'}
          </p>
        </div>
        
        <div className="overflow-y-auto p-6 flex-1">
          {step === 1 && (
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Current CGPA (Out of 10)
                </label>
                <input
                  type="number"
                  step="0.01"
                  max="10"
                  required
                  value={cgpa}
                  onChange={(e) => setCgpa(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  placeholder="e.g. 7.5"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Overall Attendance (%)
                </label>
                <input
                  type="number"
                  step="0.1"
                  max="100"
                  required
                  value={attendance}
                  onChange={(e) => setAttendance(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  placeholder="e.g. 85.5"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Active Backlogs
                </label>
                <input
                  type="number"
                  min="0"
                  required
                  value={backlogs}
                  onChange={(e) => setBacklogs(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  placeholder="e.g. 0"
                />
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6">
              {subjects.map((sub, index) => (
                <div key={index} className="p-4 rounded-xl border border-slate-200 bg-slate-50 relative">
                  <button 
                    type="button" 
                    onClick={() => handleRemoveSubject(index)}
                    className="absolute top-4 right-4 text-slate-400 hover:text-rose-500 transition"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                  <h4 className="text-xs font-bold text-slate-800 mb-3 uppercase tracking-wider">Subject #{index + 1}</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="sm:col-span-1 md:col-span-1">
                      <label className="block text-[10px] font-semibold text-slate-500 uppercase">Code</label>
                      <input type="text" placeholder="CS101" value={sub.subject_code} onChange={e => handleSubjectChange(index, 'subject_code', e.target.value)} className="mt-1 w-full px-2 py-1.5 text-xs border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none" />
                    </div>
                    <div className="sm:col-span-1 md:col-span-2">
                      <label className="block text-[10px] font-semibold text-slate-500 uppercase">Subject Name</label>
                      <input type="text" placeholder="Data Structures" value={sub.subject_name} onChange={e => handleSubjectChange(index, 'subject_name', e.target.value)} className="mt-1 w-full px-2 py-1.5 text-xs border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none" />
                    </div>
                    <div className="sm:col-span-1 md:col-span-1">
                      <label className="block text-[10px] font-semibold text-slate-500 uppercase">Credits</label>
                      <input type="number" min="1" max="10" value={sub.credits} onChange={e => handleSubjectChange(index, 'credits', e.target.value)} className="mt-1 w-full px-2 py-1.5 text-xs border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none" />
                    </div>

                    <div className="sm:col-span-1 md:col-span-1">
                      <label className="block text-[10px] font-semibold text-slate-500 uppercase">Attended Classes</label>
                      <input type="number" value={sub.classes_attended} onChange={e => handleSubjectChange(index, 'classes_attended', e.target.value)} className="mt-1 w-full px-2 py-1.5 text-xs border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none" />
                    </div>
                    <div className="sm:col-span-1 md:col-span-1">
                      <label className="block text-[10px] font-semibold text-slate-500 uppercase">Total Classes</label>
                      <input type="number" value={sub.total_classes} onChange={e => handleSubjectChange(index, 'total_classes', e.target.value)} className="mt-1 w-full px-2 py-1.5 text-xs border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none" />
                    </div>
                    <div className="sm:col-span-1 md:col-span-2 grid grid-cols-3 gap-2">
                      <div>
                        <label className="block text-[10px] font-semibold text-slate-500 uppercase truncate">Internal (50)</label>
                        <input type="number" step="0.5" value={sub.internal_marks} onChange={e => handleSubjectChange(index, 'internal_marks', e.target.value)} className="mt-1 w-full px-2 py-1.5 text-xs border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none" />
                      </div>
                      <div>
                        <label className="block text-[10px] font-semibold text-slate-500 uppercase truncate">Assign (25)</label>
                        <input type="number" step="0.5" value={sub.assignment_marks} onChange={e => handleSubjectChange(index, 'assignment_marks', e.target.value)} className="mt-1 w-full px-2 py-1.5 text-xs border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none" />
                      </div>
                      <div>
                        <label className="block text-[10px] font-semibold text-slate-500 uppercase truncate">Final (100)</label>
                        <input type="number" step="0.5" value={sub.final_exam_marks} onChange={e => handleSubjectChange(index, 'final_exam_marks', e.target.value)} className="mt-1 w-full px-2 py-1.5 text-xs border border-slate-200 rounded-md focus:border-blue-500 focus:outline-none" />
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              <button 
                type="button" 
                onClick={handleAddSubject}
                className="w-full py-3 border-2 border-dashed border-slate-300 rounded-xl text-slate-500 text-xs font-semibold flex items-center justify-center gap-2 hover:bg-slate-50 hover:border-blue-300 hover:text-blue-600 transition"
              >
                <Plus className="w-4 h-4" /> Add Enrolled Subject
              </button>
            </div>
          )}
        </div>

        <div className="bg-slate-50 p-4 border-t border-slate-200 flex justify-between shrink-0">
          {step === 2 ? (
            <button
              type="button"
              onClick={() => setStep(1)}
              className="px-4 py-2 text-xs font-semibold text-slate-600 bg-white border border-slate-200 rounded-lg hover:bg-slate-100 transition flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
          ) : (
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800 transition"
            >
              Skip
            </button>
          )}

          {step === 1 ? (
            <button
              type="button"
              onClick={() => setStep(2)}
              className="px-4 py-2 text-xs font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
            >
              Next Step <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="px-6 py-2 text-xs font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 shadow-md flex items-center gap-2"
            >
              {loading ? 'Saving Profile...' : 'Save Complete Profile'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

