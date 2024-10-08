// frontend/src/app/admin-dashboard/update-employee.tsx＝＝社員更新＝＝
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { updateEmployee, getEmployee } from '@/services/employeeService';
import { getAuth } from 'firebase/auth';
import clientLogger from '@/lib/clientLogger';
import Link from 'next/link';
import app from '@/firebase/config'; // Firebase 初期化ファイルをインポート
import '@/app/admin-dashboard/globals.css';
import Loading from '@/components/loading';
// 部署のリスト
const departments = ['営業部', '技術部', '人事部', '財務部', 'その他'];

// 役職のリスト
const positions = ['manager', 'mentor', 'その他'];

interface Employee {
  name: string;
  department: string;
  role: string;
  email: string;
}

export default function UpdateEmployee() {
  const [employee, setEmployee] = useState<Employee>({
    name: '',
    department: departments[0], // デフォルト値を設定
    role: positions[0], // デフォルト値を設定
    email: '',
  });
  const searchParams = useSearchParams();
  const employeeId = searchParams.get('employeeId');
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [adminEmail, setAdminEmail] = useState<string | null>(null);

  useEffect(() => {
    const checkAuthAndFetchData = async () => {
      const auth = getAuth(app);
      const currentUser = auth.currentUser;

      if (!currentUser) {
        router.push('/login/company');
        return;
      }

      setAdminEmail(currentUser.email || '');

      const companyId = localStorage.getItem('companyId');
      if (companyId && employeeId) {
        try {
          const data = await getEmployee(companyId, employeeId);
          if (data) {
            setEmployee(data as Employee);
          } else {
            clientLogger.error('Employee data not found.');
          }
        } catch (error) {
          clientLogger.error(`Error fetching employee data:, ${error}`);
        }
      }

      setLoading(false); // 全ての処理が完了した後にloadingをfalseに設定
    };

    checkAuthAndFetchData();
  }, [employeeId, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (employeeId) {
      try {
        const companyId = await getCompanyId();
        if (companyId) {
          await updateEmployee(companyId, employeeId, employee);
          alert('更新が完了しました');
          router.push('/admin-dashboard');
        } else {
          throw new Error('Company ID not found.');
        }
      } catch (error) {
        clientLogger.error(`Error updating employee:, ${error}`);
        alert('更新に失敗しました。もう一度お試しください。');
      }
    }
  };
  if (loading) {
    return <Loading />;
  }

  async function getCompanyId(): Promise<string | null> {
    const auth = getAuth();
    const user = auth.currentUser;
    if (user) {
      return user.uid;
    }
    return null;
  }
  return (
    <div className='my-custom-font flex min-h-screen text-[17px]   '>
      {/* 左側のナビゲーションエリア */}

      <div className='w-[400px] bg-gray-100 text-[#003366] border-r-[1px] border-[#336699] flex flex-col items-center p-4'>
        <div className='w-full flex flex-col items-center mb-6 bg-gray-200 rounded-lg p-4'>
          <img src='/logo/glay_2.png' alt='Logo' className='h-[70px] mb-1' />

          {adminEmail && (
            <div className='text-[#003366] w-full text-center'>
              <p className='mb-0'>ログイン中の管理者:</p>
              <p className='mb-4 font-bold text-[20px]'>{adminEmail}</p>
            </div>
          )}
        </div>
        <Link
          href='/admin-dashboard'
          className='w-full py-2 mb-4 border-b-[2px] border-gray-300 flex items-center block'
        >
          <span className='mr-2 '>
            <img src='/admin-dashboard/assignment.png' alt='ホーム' className='w-8 h-8' />{' '}
            {/* ホームアイコン */}
          </span>
          利用者権限一覧
        </Link>

        <Link
          href='/admin-dashboard/new-employee'
          className='w-full text py-2 mb-4 border-b-[2px] border-gray-300 flex items-center items-center block'
        >
          <span className='mr-2'>
            <img src='/admin-dashboard/person_add.png' alt='新規登録' className='w-8 h-8' />{' '}
            {/* 新規登録アイコン */}
          </span>
          新規登録
        </Link>

        <Link
          href='/'
          className='w-full text py-2 flex  border-b-[2px] border-gray-300  items-center block'
        >
          <span className='mr-2'>
            <img src='/admin-dashboard/home.png' alt='アプリTOP' className='w-8 h-8' />{' '}
            {/* アプリTOPアイコン */}
          </span>
          ホーム
        </Link>
      </div>

      {/* 右側のメインコンテンツエリア */}

      <div className='w-full flex flex-col text-[#003366] bg-white'>
        {/* 上部に社員一覧 */}
        <div className='flex-1 p-0 overflow-y-auto'>
          <div className='w-full bg-[#003366] text-white p-4 flex items-center justify-between'>
            <h1 className='text-3xl font-bold mb-4 mt-5 flex items-center'>
              <img src='/admin-dashboard/update.png' alt='新規登録' className='w-8 h-8 mr-2' />
              メンバー更新画面
            </h1>
          </div>
          <form onSubmit={handleSubmit} className='bg-white p-4 rounded shadow'>
            <div className='mb-4'>
              <label className='block text-gray-700'>氏名</label>
              <input
                type='text'
                value={employee.name}
                onChange={(e) => setEmployee({ ...employee, name: e.target.value })}
                className='w-full border p-2 rounded'
                required
              />
            </div>
            <div className='mb-4'>
              <label className='block text-gray-700'>部署</label>
              <select
                value={employee.department}
                onChange={(e) => setEmployee({ ...employee, department: e.target.value })}
                className='w-full border p-2 rounded'
                required
              >
                {departments.map((dept) => (
                  <option key={dept} value={dept}>
                    {dept}
                  </option>
                ))}
              </select>
            </div>
            <div className='mb-4'>
              <label className='block text-gray-700'>役職</label>
              <select
                value={employee.role}
                onChange={(e) => setEmployee({ ...employee, role: e.target.value })}
                className='w-full border p-2 rounded'
                required
              >
                {positions.map((pos) => (
                  <option key={pos} value={pos}>
                    {pos}
                  </option>
                ))}
              </select>
            </div>
            <div className='mb-4'>
              <label className='block text-gray-700'>メールアドレス</label>
              <div className='flex'>
                <input
                  type='text'
                  value={employee.email.split('@')[0]}
                  onChange={(e) =>
                    setEmployee({
                      ...employee,
                      email: `${e.target.value.replace(/@/g, '')}@${employee.email.split('@')[1]}`,
                    })
                  }
                  onKeyDown={(e) => {
                    if (e.key === '@') {
                      e.preventDefault();
                    }
                  }}
                  className='w-full border p-2 rounded'
                  required
                />
                <span className='p-2 bg-gray-100 border border-l-0 rounded-r'>
                  @{employee.email.split('@')[1]}
                </span>
              </div>
            </div>
            <button className='bg-[#66b2ff] text-white py-2  px-4   hover:bg-blue-500 text-[17px]  rounded-lg mr-2 font-normal  active:transform active:translate-y-1 '>
              更新
            </button>
            <Link href='/admin-dashboard'>
              <button className='bg-gray-300   hover:bg-[#c0c0c0] text-black py-2 px-4 rounded-lg ml-2 text-[17px]  active:transform active:translate-y-1 '>
                戻る
              </button>
            </Link>
          </form>
        </div>
      </div>
    </div>
  );
}
