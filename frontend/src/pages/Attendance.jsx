import { useState, useEffect } from 'react';
import { attendanceAPI, studentsAPI } from '../api';

const Attendance = () => {
  const [attendances, setAttendances] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    student_id: '',
    date: new Date().toISOString().split('T')[0],
    status: '출석',
  });
  const [filters, setFilters] = useState({
    studentName: '',
    date: '',
    status: '전체',
  });
  const [filteredData, setFilteredData] = useState([]);

  const fetchData = async () => {
    try {
      const [attendanceRes, studentsRes] = await Promise.all([
        attendanceAPI.getAll(),
        studentsAPI.getAll(),
      ]);
      setAttendances(attendanceRes.data);
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

  useEffect(() => {
    let result = attendances;

    if (filters.studentName) {
      result = result.filter((attendance) => {
        const studentName = getStudentName(attendance.student_id);
        return studentName.toLowerCase().includes(filters.studentName.toLowerCase());
      });
    }

    if (filters.date) {
      result = result.filter((attendance) =>
        attendance.date === filters.date
      );
    }

    if (filters.status && filters.status !== '전체') {
      result = result.filter((attendance) =>
        attendance.status === filters.status
      );
    }

    setFilteredData(result);
  }, [attendances, filters, students]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await attendanceAPI.create({
        ...formData,
        student_id: parseInt(formData.student_id),
      });
      setShowModal(false);
      setFormData({
        student_id: '',
        date: new Date().toISOString().split('T')[0],
        status: '출석',
      });
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || '등록에 실패했습니다.');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try {
      await attendanceAPI.delete(id);
      fetchData();
    } catch (error) {
      alert('삭제에 실패했습니다.');
    }
  };

  const getStudentName = (studentId) => {
    const student = students.find((s) => s.id === studentId);
    return student ? student.name : '알 수 없음';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case '출석':
        return 'bg-green-100 text-green-800';
      case '지각':
        return 'bg-yellow-100 text-yellow-800';
      case '결석':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleResetFilters = () => {
    setFilters({
      studentName: '',
      date: '',
      status: '전체',
    });
  };

  if (loading) {
    return <div className="text-center py-8">로딩 중...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">출결 관리</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          + 출결 등록
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">학생 이름 검색</label>
            <input
              type="text"
              value={filters.studentName}
              onChange={(e) => setFilters({ ...filters, studentName: e.target.value })}
              placeholder="학생 이름 입력"
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">날짜 필터</label>
            <input
              type="date"
              value={filters.date}
              onChange={(e) => setFilters({ ...filters, date: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">상태 필터</label>
            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            >
              <option value="전체">전체</option>
              <option value="출석">출석</option>
              <option value="지각">지각</option>
              <option value="결석">결석</option>
            </select>
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
          총 {filteredData.length}건 (전체 {attendances.length}건)
        </div>
      </div>

      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">ID</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">학생</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">날짜</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">상태</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500">관리</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {filteredData.map((attendance) => (
              <tr key={attendance.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">{attendance.id}</td>
                <td className="px-6 py-4 font-medium">
                  {getStudentName(attendance.student_id)}
                </td>
                <td className="px-6 py-4">{attendance.date}</td>
                <td className="px-6 py-4">
                  <span
                    className={`px-2 py-1 rounded-full text-sm ${getStatusColor(
                      attendance.status
                    )}`}
                  >
                    {attendance.status}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => handleDelete(attendance.id)}
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
            {attendances.length === 0 ? '출결 기록이 없습니다.' : '필터 결과가 없습니다.'}
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">출결 등록</h2>
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
                <label className="block text-sm font-medium text-gray-700 mb-1">날짜</label>
                <input
                  type="date"
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">상태</label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                >
                  <option value="출석">출석</option>
                  <option value="지각">지각</option>
                  <option value="결석">결석</option>
                </select>
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
                  등록
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Attendance;
