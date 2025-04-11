import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  InputAdornment,
  IconButton,
  Paper,
  Divider,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  LocalGasStation as GasIcon,
  People as PeopleIcon,
  Build as BuildIcon,
  TrendingUp as TrendingIcon,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Mock data for demonstration
const mockData = {
  kpis: [
    { title: 'Total Cylinders', value: '1,234', icon: <GasIcon />, color: 'primary.main' },
    { title: 'Active Customers', value: '89', icon: <PeopleIcon />, color: 'secondary.main' },
    { title: 'Maintenance Due', value: '12', icon: <BuildIcon />, color: 'warning.main' },
    { title: 'Monthly Growth', value: '+8.5%', icon: <TrendingIcon />, color: 'success.main' },
  ],
  recentMovements: [
    { id: 'CYL-001', type: 'Delivery', customer: 'ABC Corp', date: '2024-03-15' },
    { id: 'CYL-002', type: 'Return', customer: 'XYZ Ltd', date: '2024-03-14' },
    { id: 'CYL-003', type: 'Maintenance', customer: '123 Industries', date: '2024-03-13' },
  ],
  cylinderStatus: [
    { status: 'In Use', count: 850 },
    { status: 'Available', count: 300 },
    { status: 'Maintenance', count: 84 },
  ],
};

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <Box sx={{ p: 3 }}>
      {/* Header with Search */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          Dashboard
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            placeholder="Search cylinders, customers..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{ width: 300 }}
          />
          <IconButton>
            <FilterIcon />
          </IconButton>
        </Box>
      </Box>

      {/* KPI Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {mockData.kpis.map((kpi, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                p: 2,
                backgroundColor: kpi.color,
                color: 'white',
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {kpi.icon}
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    {kpi.title}
                  </Typography>
                </Box>
                <Typography variant="h4" component="div">
                  {kpi.value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Main Content */}
      <Grid container spacing={3}>
        {/* Cylinder Status Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Cylinder Status Distribution
            </Typography>
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={mockData.cylinderStatus}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="status" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill={theme.palette.primary.main} />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        {/* Recent Movements */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Recent Movements
            </Typography>
            <Box>
              {mockData.recentMovements.map((movement, index) => (
                <Box key={index}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 1 }}>
                    <Typography variant="body1">{movement.id}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {movement.date}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 1 }}>
                    <Typography variant="body2">{movement.type}</Typography>
                    <Typography variant="body2">{movement.customer}</Typography>
                  </Box>
                  {index < mockData.recentMovements.length - 1 && <Divider sx={{ my: 1 }} />}
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 