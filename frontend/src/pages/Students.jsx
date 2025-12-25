import { useState, useEffect } from 'react';
import { studentsAPI } from '../api';

const Students = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    student_number: '',
    class_name: '',
  });
  const [filters, setFilters] = useState({
    name: '',
    student_number: '',
    class_name: '',
  });
  const [filteredData, setFilteredData] = useState([]);

  const fetchStudents = async () => {
    try {
      const response = await studentsAPI.getAll();
      setStudents(response.data);
    } catch (error) {
      console.error('학생 목록 조회 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  useEffect(() => {
    let result = students;

    if (filters.name) {
      result = result.filter((student) =>
        student.name.toLowerCase().includes(filters.name.toLowerCase())
      );
    }

    if (filters.student_number) {
      result = result.filter((student) =>
        student.student_number.toLowerCase().includes(filters.student_number.toLowerCase())
      );
    }

    if (filters.class_name) {
      result = result.filter((student) =>
        student.class_name.toLowerCase().includes(filters.class_name.toLowerCase())
      );
    }

    setFilteredData(result);
  }, [students, filters]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingStudent) {
        await studentsAPI.update(editingStudent.id, formData);
      } else {
        await studentsAPI.create(formData);
      }
      setShowModal(false);
      setEditingStudent(null);
      setFormData({ name: '', student_number: '', class_name: '' });
      fetchStudents();
    } catch (error) {
      alert(error.response?.data?.detail || '저장에 실패했습니다.');
    }
  };

  const handleEdit = (student) => {
    setEditingStudent(student);
    setFormData({
      name: student.name,
      student_number: student.student_number,
      class_name: student.class_name,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try {
      await studentsAPI.delete(id);
      fetchStudents();
    } catch (error) {
      alert('삭제에 실패했습니다.');
    }
  };

  const openCreateModal = () => {
    setEditingStudent(null);
    setFormData({ name: '', student_number: '', class_name: '' });
    setShowModal(true);
  };

  const handleResetFilters = () => {
    setFilters({
      name: '',
      student_number: '',
      class_name: '',
    });
  };

  if (loading) {
    return <div className="text-center py-8">로딩 중...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">학생 관리</h1>
        <button
          onClick={openCreateModal}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          + 학생 등록
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">이름 검색</label>
            <input
              type="text"
              value={filters.name}
              onChange={(e) => setFilters({ ...filters, name: e.target.value })}
              placeholder="이름 입력"
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">학번 검색</label>
            <input
              type="text"
              value={filters.student_number}
              onChange={(e) => setFilters({ ...filters, student_number: e.target.value })}
              placeholder="학번 입력"
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">반 필터</label>
            <input
              type="text"
              value={filters.class_name}
              onChange={(e) => setFilters({ ...filters, class_name: e.target.value })}
              placeholder="반 입력"
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={handleResetFilters}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              초기화
            </button>
          </div>
        </div>
        <div className="mt-4 text-sm text-gray-600">
          총 {filteredData.length}명 (전체 {students.length}명)
        </div>
      </div>

      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">ID</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">이름</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">학번</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">반</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">관리</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {filteredData.map((student) => (
              <tr key={student.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">{student.id}</td>
                <td className="px-6 py-4 font-medium">{student.name}</td>
                <td className="px-6 py-4">{student.student_number}</td>
                <td className="px-6 py-4">{student.class_name}</td>
                <td className="px-6 py-4 space-x-2">
                  <button
                    onClick={() => handleEdit(student)}
                    className="text-blue-600 hover:underline"
                  >
                    수정
                  </button>
                  <button
                    onClick={() => handleDelete(student.id)}
                    className="text-red-600 hover:underline"
                  >
                    삭제
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filteredData.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            {students.length === 0 ? '등록된 학생이 없습니다.' : '검색 결과가 없습니다.'}
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">
              {editingStudent ? '학생 수정' : '학생 등록'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">이름</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">학번</label>
                <input
                  type="text"
                  value={formData.student_number}
                  onChange={(e) => setFormData({ ...formData, student_number: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">반</label>
                <input
                  type="text"
                  value={formData.class_name}
                  onChange={(e) => setFormData({ ...formData, class_name: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
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
                  {editingStudent ? '수정' : '등록'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Students;
