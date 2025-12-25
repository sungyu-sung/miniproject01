import { useState, useEffect } from 'react';
import { statsAPI } from '../api';
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, ResponsiveContainer
} from 'recharts';

const GRADE_COLORS = ['#22C55E', '#84CC16', '#EAB308', '#F97316', '#EF4444'];

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [attendanceData, setAttendanceData] = useState(null);
  const [gradesBySubject, setGradesBySubject] = useState([]);
  const [gradeDistribution, setGradeDistribution] = useState(null);
  const [dailyAttendance, setDailyAttendance] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dashboardRes, attendanceRes, subjectRes, distRes, dailyRes] = await Promise.all([
          statsAPI.getDashboard(),
          statsAPI.getAttendanceSummary(),
          statsAPI.getGradesBySubject(),
          statsAPI.getGradesDistribution(),
          statsAPI.getAttendanceDaily(14),
        ]);
        setDashboardData(dashboardRes.data);
        setAttendanceData(attendanceRes.data);
        setGradesBySubject(subjectRes.data);
        setGradeDistribution(distRes.data);
        setDailyAttendance(dailyRes.data);
      } catch (error) {
        console.error('Data loading failed:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (<div className="flex items-center justify-center h-64"><div className="text-gray-500">Loading...</div></div>);
  }

  const attendancePieData = attendanceData ? [
    { name: 'Present', value: attendanceData.present, color: '#10B981' },
    { name: 'Late', value: attendanceData.late, color: '#F59E0B' },
    { name: 'Absent', value: attendanceData.absent, color: '#EF4444' },
  ].filter(d => d.value > 0) : [];

  const gradeDistData = gradeDistribution ? [
    { grade: 'A', count: gradeDistribution.A },
    { grade: 'B', count: gradeDistribution.B },
    { grade: 'C', count: gradeDistribution.C },
    { grade: 'D', count: gradeDistribution.D },
    { grade: 'F', count: gradeDistribution.F },
  ] : [];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl shadow p-6">
          <p className="text-gray-500 text-sm">Total Students</p>
          <p className="text-3xl font-bold text-gray-800">{dashboardData?.student_count || 0}</p>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <p className="text-gray-500 text-sm">Today Present</p>
          <p className="text-3xl font-bold text-green-600">{dashboardData?.today_attendance?.present || 0}</p>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <p className="text-gray-500 text-sm">Average Score</p>
          <p className="text-3xl font-bold text-blue-600">{dashboardData?.average_score || 0}</p>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <p className="text-gray-500 text-sm">Total Records</p>
          <p className="text-3xl font-bold text-purple-600">{dashboardData?.total_grades || 0}</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Attendance Overview</h2>
          {attendancePieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={attendancePieData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value">
                  {attendancePieData.map((entry, index) => (<Cell key={index} fill={entry.color} />))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (<div className="h-64 flex items-center justify-center text-gray-400">No data</div>)}
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Grade Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={gradeDistData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="grade" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3B82F6">
                {gradeDistData.map((entry, index) => (<Cell key={index} fill={GRADE_COLORS[index]} />))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Attendance Trend</h2>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={dailyAttendance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="present" stroke="#10B981" name="Present" />
              <Line type="monotone" dataKey="late" stroke="#F59E0B" name="Late" />
              <Line type="monotone" dataKey="absent" stroke="#EF4444" name="Absent" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Subject Averages</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={gradesBySubject} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis dataKey="subject" type="category" width={60} />
              <Tooltip />
              <Bar dataKey="average" fill="#6366F1" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      {dashboardData?.class_distribution && (
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Students by Class</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
            {dashboardData.class_distribution.map((cls) => (
              <div key={cls.class_name} className="bg-gray-50 rounded-lg p-4 text-center">
                <p className="text-lg font-bold text-indigo-600">{cls.class_name}</p>
                <p className="text-2xl font-bold text-gray-800">{cls.count}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
