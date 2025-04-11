import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  InputAdornment,
  IconButton,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const Cylinders = () => {
  const [searchQuery, setSearchQuery] = useState('');

  // Sample data - would normally come from your API
  const cylinders = [
    {
      id: 1,
      serialNumber: 'CYL001',
      type: 'Oxygen',
      capacity: '50L',
      status: 'In Service',
      currentLocation: 'Warehouse A',
      lastInspection: '2024-01-15',
    },
    {
      id: 2,
      serialNumber: 'CYL002',
      type: 'Nitrogen',
      capacity: '40L',
      status: 'In Transit',
      currentLocation: 'Delivery Truck 1',
      lastInspection: '2024-01-10',
    },
    // Add more sample data as needed
  ];

  const columns: GridColDef[] = [
    { field: 'serialNumber', headerName: 'Serial Number', width: 150 },
    { field: 'type', headerName: 'Type', width: 120 },
    { field: 'capacity', headerName: 'Capacity', width: 100 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'currentLocation', headerName: 'Current Location', width: 180 },
    { field: 'lastInspection', headerName: 'Last Inspection', width: 150 },
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
            Delete
          </Button>
        </Box>
      ),
    },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Cylinders</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // Handle add new cylinder
          }}
        >
          Add Cylinder
        </Button>
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search cylinders..."
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
          rows={cylinders}
          columns={columns}
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

export default Cylinders; 