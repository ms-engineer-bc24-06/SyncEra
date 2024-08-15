// components/AuthRoute.tsx
import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuthState } from '@/app/hooks/auth/useAuthState';
import clientLogger from '@/lib/clientLogger';

interface AuthRouteProps {
  children: React.ReactNode;
  requiredRole: string;
}

const AuthRoute: React.FC<AuthRouteProps> = ({ children, requiredRole }) => {
  const { user, loading, error, role } = useAuthState();
  const router = useRouter();

  React.useEffect(() => {
    if (!loading) {
      if (!user) {
        clientLogger.error(`===ユーザーが一致しませんでした。===`);
        router.push('/login/employee');
      } else if (role !== requiredRole) {
        clientLogger.error(`===役職が一致しませんでした。===`);
        switch (role) {
          case 'staff':
            router.push('/staff-dashboard');
            break;
          case 'employee':
            router.push('/employee-dashboard');
            break;
          default:
            router.push('/login/employee');
        }
      }
    }
  }, [user, loading, role, requiredRole, router]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!user || role !== requiredRole) {
    return null;
  }

  return <>{children}</>;
};

export default AuthRoute;
