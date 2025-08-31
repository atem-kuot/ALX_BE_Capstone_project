import React, { useState, useEffect } from 'react';
import { Card, Badge, Alert, Button, Form, InputGroup } from 'react-bootstrap';
import { FiBell, FiFilter, FiSearch, FiCheck, FiClock, FiAlertTriangle, FiCalendar } from 'react-icons/fi';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    status: 'all',
    type: 'all',
    priority: 'all'
  });

  // Mock data - replace with actual API call
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        // Simulate API call
        setTimeout(() => {
          const mockAlerts = [
            {
              id: 1,
              title: 'Low Stock Alert',
              message: 'Amoxicillin 500mg is running low (15 units remaining)',
              type: 'stock',
              priority: 'high',
              status: 'pending',
              itemId: 1,
              itemName: 'Amoxicillin 500mg',
              createdAt: '2023-08-30T14:30:00Z',
              updatedAt: '2023-08-30T14:30:00Z'
            },
            {
              id: 2,
              title: 'Expiration Warning',
              message: 'Ibuprofen 200mg expires in 30 days',
              type: 'expiry',
              priority: 'medium',
              status: 'pending',
              itemId: 2,
              itemName: 'Ibuprofen 200mg',
              createdAt: '2023-08-29T09:15:00Z',
              updatedAt: '2023-08-29T09:15:00Z'
            },
            {
              id: 3,
              title: 'Restock Completed',
              message: 'Paracetamol 500mg has been restocked (1000 units added)',
              type: 'restock',
              priority: 'low',
              status: 'resolved',
              itemId: 3,
              itemName: 'Paracetamol 500mg',
              createdAt: '2023-08-28T11:20:00Z',
              updatedAt: '2023-08-28T11:20:00Z',
              resolvedAt: '2023-08-28T11:20:00Z'
            }
          ];
          setAlerts(mockAlerts);
          setLoading(false);
        }, 800);
      } catch (error) {
        console.error('Error fetching alerts:', error);
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleFilterChange = (filterName, value) => {
    setFilters({
      ...filters,
      [filterName]: value
    });
  };

  const markAsResolved = (id) => {
    setAlerts(alerts.map(alert => 
      alert.id === id 
        ? { ...alert, status: 'resolved', resolvedAt: new Date().toISOString() }
        : alert
    ));
  };

  const getPriorityBadge = (priority) => {
    const variants = {
      high: 'danger',
      medium: 'warning',
      low: 'info'
    };
    return (
      <Badge bg={variants[priority]} className="text-capitalize">
        {priority}
      </Badge>
    );
  };\n
  const getStatusBadge = (status) => {
    const variants = {
      pending: 'warning',
      resolved: 'success',
      in_progress: 'primary'
    };
    return (
      <Badge bg={variants[status]} className="text-capitalize">
        {status.replace('_', ' ')}
      </Badge>
    );
  };

  const getTypeIcon = (type) => {
    const icons = {
      stock: <FiAlertTriangle className="text-warning me-1" />,
      expiry: <FiCalendar className="text-danger me-1" />,
      restock: <FiCheck className="text-success me-1" />,
      default: <FiBell className="text-primary me-1" />
    };
    return icons[type] || icons.default;
  };

  const filteredAlerts = alerts.filter(alert => {
    const matchesSearch = 
      alert.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      alert.message.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilters = 
      (filters.status === 'all' || alert.status === filters.status) &&
      (filters.type === 'all' || alert.type === filters.type) &&
      (filters.priority === 'all' || alert.priority === filters.priority);
    
    return matchesSearch && matchesFilters;
  });

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '300px' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="alerts">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Alerts & Notifications</h2>
        <div className="d-flex gap-2">
          <Button variant="outline-secondary" size="sm">
            <FiFilter className="me-1" /> Filter
          </Button>
          <div style={{ minWidth: '250px' }}>
            <InputGroup size="sm">
              <InputGroup.Text>
                <FiSearch />
              </InputGroup.Text>
              <Form.Control
                type="text"
                placeholder="Search alerts..."
                value={searchTerm}
                onChange={handleSearch}
              />
            </InputGroup>
          </div>
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-md-3">
          <Form.Group>
            <Form.Label>Status</Form.Label>
            <Form.Select 
              size="sm"
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
            >
              <option value="all">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
            </Form.Select>
          </Form.Group>
        </div>
        <div className="col-md-3">
          <Form.Group>
            <Form.Label>Type</Form.Label>
            <Form.Select 
              size="sm"
              value={filters.type}
              onChange={(e) => handleFilterChange('type', e.target.value)}
            >
              <option value="all">All Types</option>
              <option value="stock">Low Stock</option>
              <option value="expiry">Expiry</option>
              <option value="restock">Restock</option>
            </Form.Select>
          </Form.Group>
        </div>
        <div className="col-md-3">
          <Form.Group>
            <Form.Label>Priority</Form.Label>
            <Form.Select 
              size="sm"
              value={filters.priority}
              onChange={(e) => handleFilterChange('priority', e.target.value)}
            >
              <option value="all">All Priorities</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </Form.Select>
          </Form.Group>
        </div>
      </div>

      {filteredAlerts.length === 0 ? (
        <Alert variant="info">
          No alerts found matching your criteria.
        </Alert>
      ) : (
        <div className="alert-list">
          {filteredAlerts.map(alert => (
            <Card key={alert.id} className="mb-3 border-start-0 border-end-0 border-top-0 border-3" 
              style={{ 
                borderBottomColor: alert.status === 'resolved' ? '#198754' : 
                                 alert.priority === 'high' ? '#dc3545' :
                                 alert.priority === 'medium' ? '#ffc107' : '#0d6efd'
              }}>
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start">
                  <div>
                    <div className="d-flex align-items-center mb-1">
                      {getTypeIcon(alert.type)}
                      <h5 className="mb-0 me-2">{alert.title}</h5>
                      {getPriorityBadge(alert.priority)}
                      <span className="ms-2">{getStatusBadge(alert.status)}</span>
                    </div>
                    <p className="mb-1">{alert.message}</p>
                    <small className="text-muted">
                      <FiClock className="me-1" />
                      {new Date(alert.createdAt).toLocaleString()}
                    </small>
                  </div>
                  {alert.status !== 'resolved' && (
                    <Button 
                      variant="outline-success" 
                      size="sm"
                      onClick={() => markAsResolved(alert.id)}
                    >
                      Mark as Resolved
                    </Button>
                  )}
                </div>
              </Card.Body>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Alerts;
