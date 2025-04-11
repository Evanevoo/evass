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
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const Movements = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState(0);

  // Sample data - would normally come from your API
  const movements = [
    {
      id: 1,
      cylinderId: 'CYL001',
      type: 'Delivery',
      fromLocation: 'Warehouse A',
      toLocation: 'ABC Hospital',
      date: '2024-01-15',
      status: 'Completed',
      driver: 'John Doe',
    },
    {
      id: 2,
      cylinderId: 'CYL002',
      type: 'Return',
      fromLocation: 'XYZ Manufacturing',
      toLocation: 'Warehouse A',
      date: '2024-01-16',
      status: 'In Progress',
      driver: 'Jane Smith',
    },
  ];

  const transactions = [
    {
      id: 1,
      customer: 'ABC Hospital',
      date: '2024-01-15',
      type: 'Delivery',
      cylinders: 5,
      totalAmount: 250.00,
      status: 'Completed',
    },
    {
      id: 2,
      customer: 'XYZ Manufacturing',
      date: '2024-01-16',
      type: 'Return',
      cylinders: 3,
      totalAmount: 150.00,
      status: 'Pending',
    },
  ];

  const movementColumns: GridColDef[] = [
    { field: 'cylinderId', headerName: 'Cylinder ID', width: 120 },
    { field: 'type', headerName: 'Type', width: 120 },
    { field: 'fromLocation', headerName: 'From', width: 180 },
    { field: 'toLocation', headerName: 'To', width: 180 },
    { field: 'date', headerName: 'Date', width: 120 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'driver', headerName: 'Driver', width: 150 },
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

  const transactionColumns: GridColDef[] = [
    { field: 'customer', headerName: 'Customer', width: 200 },
    { field: 'date', headerName: 'Date', width: 120 },
    { field: 'type', headerName: 'Type', width: 120 },
    { field: 'cylinders', headerName: 'Cylinders', width: 100 },
    { field: 'totalAmount', headerName: 'Total Amount', width: 120 },
    { field: 'status', headerName: 'Status', width: 120 },
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

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Movements</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // Handle add new movement/transaction
          }}
        >
          {activeTab === 0 ? 'Add Movement' : 'Add Transaction'}
        </Button>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Cylinder Movements" />
          <Tab label="Transactions" />
        </Tabs>
      </Paper>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder={`Search ${activeTab === 0 ? 'movements' : 'transactions'}...`}
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
          rows={activeTab === 0 ? movements : transactions}
          columns={activeTab === 0 ? movementColumns : transactionColumns}
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

export default Movements; 