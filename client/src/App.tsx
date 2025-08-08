import { Switch, Route, useLocation } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useAuth, AuthProvider } from "./hooks/use-auth";
import { ThemeProvider } from "./hooks/use-theme";
import LoginPage from "./pages/login";
import DashboardPage from "./pages/dashboard";
import SearchPage from "./pages/search";
import AdminPage from "./pages/admin";
import Sidebar from "./components/layout/sidebar";
import TopBar from "./components/layout/top-bar";
import NotFound from "@/pages/not-found";

function Router() {
  const { user, isLoading } = useAuth();
  const [location] = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  const isLoginPage = location === "/login" || location === "/";

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-800">
      {!isLoginPage && <Sidebar />}
      
      <div className={!isLoginPage ? "lg:ml-64" : ""}>
        {!isLoginPage && <TopBar />}
        
        <main className={!isLoginPage ? "p-6" : ""}>
          <Switch>
            <Route path="/" component={DashboardPage} />
            <Route path="/dashboard" component={DashboardPage} />
            <Route path="/search" component={SearchPage} />
            <Route path="/admin" component={AdminPage} />
            <Route component={NotFound} />
          </Switch>
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          <TooltipProvider>
            <Toaster />
            <Router />
          </TooltipProvider>
        </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
