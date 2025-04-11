import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts';

interface PieLabelProps {
  name: string;
  percent: number;
}

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('month');

  // Sample data - would normally come from your API
  const cylinderUsageData = [
    { name: 'Jan', oxygen: 4000, nitrogen: 2400, argon: 2400 },
    { name: 'Feb', oxygen: 3000, nitrogen: 1398, argon: 2210 },
    { name: 'Mar', oxygen: 2000, nitrogen: 9800, argon: 2290 },
    { name: 'Apr', oxygen: 2780, nitrogen: 3908, argon: 2000 },
    { name: 'May', oxygen: 1890, nitrogen: 4800, argon: 2181 },
    { name: 'Jun', oxygen: 2390, nitrogen: 3800, argon: 2500 },
  ];

  const customerDistributionData = [
    { name: 'Hospitals', value: 35 },
    { name: 'Manufacturing', value: 25 },
    { name: 'Research', value: 20 },
    { name: 'Other', value: 20 },
  ];

  const maintenanceData = [
    { name: 'Jan', inspections: 4000, tests: 2400 },
    { name: 'Feb', inspections: 3000, tests: 1398 },
    { name: 'Mar', inspections: 2000, tests: 9800 },
    { name: 'Apr', inspections: 2780, tests: 3908 },
    { name: 'May', inspections: 1890, tests: 4800 },
    { name: 'Jun', inspections: 2390, tests: 3800 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  const metrics = [
    { title: 'Total Cylinders', value: '1,234', change: '+12%' },
    { title: 'Active Customers', value: '456', change: '+8%' },
    { title: 'Monthly Revenue', value: '$45,678', change: '+15%' },
    { title: 'Maintenance Due', value: '23', change: '-5%' },
  ];

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Analytics</Typography>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Time Range</InputLabel>
          <Select
            value={timeRange}
            label="Time Range"
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <MenuItem value="week">Last Week</MenuItem>
            <MenuItem value="month">Last Month</MenuItem>
            <MenuItem value="quarter">Last Quarter</MenuItem>
            <MenuItem value="year">Last Year</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  {metric.title}
                </Typography>
                <Typography variant="h5" component="div">
                  {metric.value}
                </Typography>
                <Typography
                  variant="body2"
                  color={metric.change.startsWith('+') ? 'success.main' : 'error.main'}
                >
                  {metric.change} from previous period
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Cylinder Usage by Type
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={cylinderUsageData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="oxygen" fill="#8884d8" />
                <Bar dataKey="nitrogen" fill="#82ca9d" />
                <Bar dataKey="argon" fill="#ffc658" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Customer Distribution
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={customerDistributionData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }: PieLabelProps) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {customerDistributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Maintenance Activities
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={maintenanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="inspections"
                  stroke="#8884d8"
                  activeDot={{ r: 8 }}
                />
                <Line type="monotone" dataKey="tests" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics; 