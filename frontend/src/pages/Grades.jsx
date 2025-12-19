import { useState, useEffect } from 'react';
import { gradesAPI, studentsAPI } from '../api';

const Grades = () => {
  const [grades, setGrades] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingGrade, setEditingGrade] = useState(null);
  const [formData, setFormData] = useState({
    student_id: '',
    subject: '',
    score: '',
  });

  const fetchData = async () => {
    try {
      const [gradesRes, studentsRes] = await Promise.all([
        gradesAPI.getAll(),
        studentsAPI.getAll(),
      ]);
      setGrades(gradesRes.data);
      setStudents(studentsRes.data);
    } catch (error) {
      console.error('데이터 조회 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        ...formData,
        student_id: parseInt(formData.student_id),
        score: parseInt(formData.score),
      };
      if (editingGrade) {
        await gradesAPI.update(editingGrade.id, data);
      } else {
        await gradesAPI.create(data);
      }
      setShowModal(false);
      setEditingGrade(null);
      setFormData({ student_id: '', subject: '', score: '' });
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || '저장에 실패했습니다.');
    }
  };

  const handleEdit = (grade) => {
    setEditingGrade(grade);
    setFormData({
      student_id: grade.student_id.toString(),
      subject: grade.subject,
      score: grade.score.toString(),
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try {
      await gradesAPI.delete(id);
      fetchData();
    } catch (error) {
      alert('삭제에 실패했습니다.');
    }
  };

  const openCreateModal = () => {
    setEditingGrade(null);
    setFormData({ student_id: '', subject: '', score: '' });
    setShowModal(true);
  };

  const getStudentName = (studentId) => {
    const student = students.find((s) => s.id === studentId);
    return student ? student.name : '알 수 없음';
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return <div className="text-center py-8">로딩 중...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">성적 관리</h1>
        <button
          onClick={openCreateModal}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          + 성적 등록
        </button>
      </div>

      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">ID</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">학생</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">과목</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">점수</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">관리</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {grades.map((grade) => (
              <tr key={grade.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">{grade.id}</td>
                <td className="px-6 py-4 font-medium">{getStudentName(grade.student_id)}</td>
                <td className="px-6 py-4">{grade.subject}</td>
                <td className={`px-6 py-4 font-bold ${getScoreColor(grade.score)}`}>
                  {grade.score}
                </td>
                <td className="px-6 py-4 space-x-2">
                  <button
                    onClick={() => handleEdit(grade)}
                    className="text-blue-600 hover:underline"
                  >
                    수정
                  </button>
                  <button
                    onClick={() => handleDelete(grade.id)}
                    className="text-red-600 hover:underline"
                  >
                    삭제
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {grades.length === 0 && (
          <div className="text-center py-8 text-gray-500">성적 기록이 없습니다.</div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">
              {editingGrade ? '성적 수정' : '성적 등록'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">학생</label>
                <select
                  value={formData.student_id}
                  onChange={(e) => setFormData({ ...formData, student_id: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  required
                >
                  <option value="">학생 선택</option>
                  {students.map((student) => (
                    <option key={student.id} value={student.id}>
                      {student.name} ({student.student_number})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">과목</label>
                <input
                  type="text"
                  value={formData.subject}
                  onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="예: 국어, 수학, 영어"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">점수</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={formData.score}
                  onChange={(e) => setFormData({ ...formData, score: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="0 ~ 100"
                  required
                />
              </div>
              <div className="flex gap-2 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50"
                >
                  취소
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {editingGrade ? '수정' : '등록'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Grades;
