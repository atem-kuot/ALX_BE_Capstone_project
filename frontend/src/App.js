import React, { useState, useEffect } from 'react';
import { Container, Navbar, Nav, Row, Col, Spinner } from 'react-bootstrap';
import './App.css';

// Components
import Dashboard from './components/Dashboard';
import Medicines from './components/Medicines';
import Alerts from './components/Alerts';
import Prescriptions from './components/Prescriptions';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  const renderContent = () => {
    switch (activeTab) {
      case 'medicines':
        return <Medicines />;
      case 'alerts':
        return <Alerts />;
      case 'prescriptions':
        return <Prescriptions />;
      default:
        return <Dashboard />;
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  return (
    <div className="App">
      <Navbar bg="primary" variant="dark" expand="lg" className="mb-4">
        <Container>
          <Navbar.Brand href="#">
            <i className="bi bi-capsule me-2"></i>
            Pharmacy Inventory
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')}>
                <i className="bi bi-speedometer2 me-1"></i> Dashboard
              </Nav.Link>
              <Nav.Link active={activeTab === 'medicines'} onClick={() => setActiveTab('medicines')}>
                <i className="bi bi-capsule me-1"></i> Medicines
              </Nav.Link>
              <Nav.Link active={activeTab === 'prescriptions'} onClick={() => setActiveTab('prescriptions')}>
                <i className="bi bi-journal-text me-1"></i> Prescriptions
              </Nav.Link>
              <Nav.Link active={activeTab === 'alerts'} onClick={() => setActiveTab('alerts')}>
                <i className="bi bi-bell me-1"></i> Alerts
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container>
        {renderContent()}
      </Container>

      <footer className="mt-5 py-3 bg-light">
        <Container>
          <p className="text-center text-muted mb-0">
            &copy; {new Date().getFullYear()} Pharmacy Inventory System
          </p>
        </Container>
      </footer>
    </div>
  );
}

export default App;
