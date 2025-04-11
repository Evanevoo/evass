import { Link } from 'react-router-dom';
import { ListItem, ListItemIcon, ListItemText } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import LocalGasStationIcon from '@mui/icons-material/LocalGasStation';
import PeopleIcon from '@mui/icons-material/People';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import AssessmentIcon from '@mui/icons-material/Assessment';

interface NavigationItemProps {
  to: string;
  text: string;
}

const NavigationItem = ({ to, text }: NavigationItemProps) => {
  const getIcon = () => {
    switch (text.toLowerCase()) {
      case 'dashboard':
        return <DashboardIcon />;
      case 'locations':
        return <LocationOnIcon />;
      case 'cylinders':
        return <LocalGasStationIcon />;
      case 'customers':
        return <PeopleIcon />;
      case 'deliveries':
        return <LocalShippingIcon />;
      case 'reports':
        return <AssessmentIcon />;
      default:
        return <DashboardIcon />;
    }
  };

  return (
    <ListItem button component={Link} to={to}>
      <ListItemIcon>{getIcon()}</ListItemIcon>
      <ListItemText primary={text} />
    </ListItem>
  );
};

export default NavigationItem; 