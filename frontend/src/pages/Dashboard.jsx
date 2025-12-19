import { useState, useEffect } from 'react';
import { studentsAPI, attendanceAPI, gradesAPI } from '../api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalStudents: 0,
    todayAttendance: 0,
    averageGrade: 0,
  });
  const [recentStudents, setRecentStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [studentsRes, attendanceRes, gradesRes] = await Promise.all([
          studentsAPI.getAll(),
          attendanceAPI.getAll(),
          gradesAPI.getAll(),
        ]);

        const students = studentsRes.data;
        const attendances = attendanceRes.data;
        const grades = gradesRes.data;

        // 통계 계산
        const today = new Date().toISOString().split('T')[0];
        const todayAttendance = attendances.filter(
          (a) => a.date === today && a.status === '출석'
        ).length;

        const avgGrade = grades.length
          ? (grades.reduce((sum, g) => sum + g.score, 0) / grades.length).toFixed(1)
          : 0;

        setStats({
          totalStudents: students.length,
          todayAttendance,
          averageGrade: avgGrade,
        });

        setRecentStudents(students.slice(0, 5));
      } catch (error) {
        console.error('데이터 로딩 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">대시보드</h1>

      {/* 통계 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">전체 학생 수</p>
              <p className="text-3xl font-bold text-gray-800">{stats.totalStudents}</p>
            </div>
            <div className="text-4xl">👨‍🎓</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">오늘 출석</p>
              <p className="text-3xl font-bold text-green-600">{stats.todayAttendance}</p>
            </div>
            <div className="text-4xl">✅</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">평균 성적</p>
              <p className="text-3xl font-bold text-blue-600">{stats.averageGrade}</p>
            </div>
            <div className="text-4xl">📊</div>
          </div>
        </div>
      </div>

      {/* 최근 등록 학생 */}
      <div className="bg-white rounded-xl shadow">
        <div className="p-6 border-b">
          <h2 className="text-lg font-semibold text-gray-800">최근 등록 학생</h2>
        </div>
        <div className="p-6">
          {recentStudents.length === 0 ? (
            <p className="text-gray-500 text-center py-4">등록된 학생이 없습니다.</p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="text-left text-gray-500 text-sm">
                  <th className="pb-3">이름</th>
                  <th className="pb-3">학번</th>
                  <th className="pb-3">반</th>
                </tr>
              </thead>
              <tbody>
                {recentStudents.map((student) => (
                  <tr key={student.id} className="border-t">
                    <td className="py-3">{student.name}</td>
                    <td className="py-3">{student.student_number}</td>
                    <td className="py-3">{student.class_name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
