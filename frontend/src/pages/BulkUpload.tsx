import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Container,
  Grid,
} from '@mui/material';

const BulkUpload: React.FC = () => {
  return (
    <Box sx={{ 
      minHeight: '100vh',
      bgcolor: 'background.default',
      py: 4
    }}>
      <Container maxWidth="lg">
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h4" component="h1" gutterBottom>
              Bulk Upload
            </Typography>
          </Grid>
          
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="body1" color="text.secondary">
                  This feature is currently under maintenance. Please check back later.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default BulkUpload; 