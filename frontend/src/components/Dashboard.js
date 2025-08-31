import React from 'react';
import { Card, Row, Col } from 'react-bootstrap';

const Dashboard = () => {
  // Mock data - replace with actual API calls
  const stats = [
    { title: 'Total Medicines', value: '245', icon: 'capsule', color: 'primary' },
    { title: 'Low Stock Alerts', value: '12', icon: 'exclamation-triangle', color: 'warning' },
    { title: 'Today\'s Prescriptions', value: '8', icon: 'file-text', color: 'success' },
    { title: 'Expiring Soon', value: '5', icon: 'clock', color: 'danger' },
  ];

  return (
    <div className="dashboard">
      <h2 className="mb-4">Dashboard</h2>
      
      <Row className="g-4 mb-4">
        {stats.map((stat, index) => (
          <Col md={3} key={index}>
            <Card className="h-100 shadow-sm">
              <Card.Body className="d-flex align-items-center">
                <div className={`bg-${stat.color}-subtle p-3 rounded me-3`}>
                  <i className={`bi bi-${stat.icon} text-${stat.color}`} style={{ fontSize: '2rem' }}></i>
                </div>
                <div>
                  <h6 className="text-muted mb-1">{stat.title}</h6>
                  <h3 className="mb-0">{stat.value}</h3>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Row className="g-4">
        <Col md={8}>
          <Card className="h-100 shadow-sm">
            <Card.Body>
              <Card.Title>Recent Activity</Card.Title>
              <div className="list-group list-group-flush">
                {[1, 2, 3, 4, 5].map((item) => (
                  <div key={item} className="list-group-item border-0 px-0">
                    <div className="d-flex w-100 justify-content-between">
                      <h6 className="mb-1">New prescription added</h6>
                      <small className="text-muted">3 mins ago</small>
                    </div>
                    <p className="mb-1">Patient: John Doe - Amoxicillin 500mg</p>
                  </div>
                ))}
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="h-100 shadow-sm">
            <Card.Body>
              <Card.Title>Quick Actions</Card.Title>
              <div className="d-grid gap-2">
                <button className="btn btn-outline-primary btn-sm mb-2">
                  <i className="bi bi-plus-circle me-2"></i>Add New Medicine
                </button>
                <button className="btn btn-outline-success btn-sm mb-2">
                  <i className="bi bi-file-earmark-plus me-2"></i>New Prescription
                </button>
                <button className="btn btn-outline-info btn-sm mb-2">
                  <i className="bi bi-bell me-2"></i>View All Alerts
                </button>
                <button className="btn btn-outline-secondary btn-sm">
                  <i className="bi bi-graph-up me-2"></i>Generate Report
                </button>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
