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

const Customers = () => {
  const [searchQuery, setSearchQuery] = useState('');

  // Sample data - would normally come from your API
  const customers = [
    {
      id: 1,
      name: 'ABC Hospital',
      email: 'contact@abchospital.com',
      phone: '+1 234-567-8901',
      address: '123 Medical St, City, State',
      type: 'Hospital',
      status: 'Active',
    },
    {
      id: 2,
      name: 'XYZ Manufacturing',
      email: 'info@xyzmanufacturing.com',
      phone: '+1 234-567-8902',
      address: '456 Industrial Ave, City, State',
      type: 'Manufacturing',
      status: 'Active',
    },
    // Add more sample data as needed
  ];

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Customer Name', width: 200 },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'phone', headerName: 'Phone', width: 150 },
    { field: 'address', headerName: 'Address', width: 250 },
    { field: 'type', headerName: 'Type', width: 150 },
    { field: 'status', headerName: 'Status', width: 120 },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 200,
      renderCell: (params) => (
        <Box>
          <Button size="small" variant="outlined" sx={{ mr: 1 }}>
            View
          </Button>
          <Button size="small" variant="outlined" sx={{ mr: 1 }}>
            Edit
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
        <Typography variant="h4">Customers</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // Handle add new customer
          }}
        >
          Add Customer
        </Button>
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search customers..."
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
          rows={customers}
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

export default Customers; 