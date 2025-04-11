import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  InputAdornment,
  Tabs,
  Tab,
  Chip,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const Maintenance = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState(0);

  // Sample data - would normally come from your API
  const maintenanceRecords = [
    {
      id: 1,
      cylinderId: 'CYL001',
      type: 'Inspection',
      date: '2024-01-15',
      dueDate: '2024-07-15',
      status: 'Completed',
      technician: 'John Doe',
      notes: 'Regular inspection completed',
    },
    {
      id: 2,
      cylinderId: 'CYL002',
      type: 'Hydrostatic Test',
      date: '2024-01-16',
      dueDate: '2024-07-16',
      status: 'Scheduled',
      technician: 'Jane Smith',
      notes: 'Scheduled for next week',
    },
  ];

  const upcomingMaintenance = [
    {
      id: 1,
      cylinderId: 'CYL001',
      type: 'Inspection',
      dueDate: '2024-07-15',
      daysRemaining: 180,
      priority: 'Medium',
    },
    {
      id: 2,
      cylinderId: 'CYL002',
      type: 'Hydrostatic Test',
      dueDate: '2024-07-16',
      daysRemaining: 181,
      priority: 'High',
    },
  ];

  const maintenanceColumns: GridColDef[] = [
    { field: 'cylinderId', headerName: 'Cylinder ID', width: 120 },
    { field: 'type', headerName: 'Type', width: 120 },
    { field: 'date', headerName: 'Date', width: 120 },
    { field: 'dueDate', headerName: 'Due Date', width: 120 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'technician', headerName: 'Technician', width: 150 },
    { field: 'notes', headerName: 'Notes', width: 200 },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <Box>
          <Button size="small" variant="outlined" sx={{ mr: 1 }}>
            View
          </Button>
          <Button size="small" variant="outlined" color="error">
            Cancel
          </Button>
        </Box>
      ),
    },
  ];

  const upcomingColumns: GridColDef[] = [
    { field: 'cylinderId', headerName: 'Cylinder ID', width: 120 },
    { field: 'type', headerName: 'Type', width: 120 },
    { field: 'dueDate', headerName: 'Due Date', width: 120 },
    { field: 'daysRemaining', headerName: 'Days Remaining', width: 120 },
    {
      field: 'priority',
      headerName: 'Priority',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={
            params.value === 'High'
              ? 'error'
              : params.value === 'Medium'
              ? 'warning'
              : 'success'
          }
          size="small"
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <Box>
          <Button size="small" variant="outlined" sx={{ mr: 1 }}>
            Schedule
          </Button>
          <Button size="small" variant="outlined">
            Details
          </Button>
        </Box>
      ),
    },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Maintenance</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // Handle add new maintenance record
          }}
        >
          {activeTab === 0 ? 'Add Record' : 'Schedule Maintenance'}
        </Button>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Maintenance Records" />
          <Tab label="Upcoming Maintenance" />
        </Tabs>
      </Paper>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder={`Search ${activeTab === 0 ? 'records' : 'upcoming maintenance'}...`}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
          <Button
            variant="outlined"
            startIcon={<FilterIcon />}
            onClick={() => {
              // Handle filter dialog
            }}
          >
            Filter
          </Button>
        </Box>
      </Paper>

      <Paper sx={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={activeTab === 0 ? maintenanceRecords : upcomingMaintenance}
          columns={activeTab === 0 ? maintenanceColumns : upcomingColumns}
          initialState={{
            pagination: {
              paginationModel: {
                pageSize: 5,
              },
            },
          }}
          pageSizeOptions={[5, 10, 25]}
          checkboxSelection
          disableRowSelectionOnClick
        />
      </Paper>
    </Box>
  );
};

export default Maintenance; 