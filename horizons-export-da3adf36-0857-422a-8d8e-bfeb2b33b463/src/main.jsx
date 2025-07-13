import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import App from '@/App';
import '@/index.css';
import { AuthProvider } from '@/contexts/SupabaseAuthContext';
import { SupabaseProvider } from '@/contexts/SupabaseClientProvider';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <HelmetProvider>
      <BrowserRouter>
        <SupabaseProvider>
          <AuthProvider>
            <App />
          </AuthProvider>
        </SupabaseProvider>
      </BrowserRouter>
    </HelmetProvider>
  </React.StrictMode>
);