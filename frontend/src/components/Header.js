import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Badge,
  Box,
} from '@mui/material';
import {
  Favorite as FavoriteIcon,
  ShoppingCart as ShoppingCartIcon,
} from '@mui/icons-material';
import { logout } from '../store/slices/authSlice';

export const Header = () => {
  const dispatch = useDispatch();
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const favoritesCount = useSelector((state) => state.favorites.items.length);
  const shoppingListCount = useSelector((state) => state.shoppingList.items.length);

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}
        >
          Foodgram
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {isAuthenticated ? (
            <>
              <IconButton
                component={RouterLink}
                to="/favorites"
                color="inherit"
              >
                <Badge badgeContent={favoritesCount} color="secondary">
                  <FavoriteIcon />
                </Badge>
              </IconButton>
              <IconButton
                component={RouterLink}
                to="/shopping-list"
                color="inherit"
              >
                <Badge badgeContent={shoppingListCount} color="secondary">
                  <ShoppingCartIcon />
                </Badge>
              </IconButton>
              <Button
                component={RouterLink}
                to="/profile"
                color="inherit"
              >
                Profile
              </Button>
              <Button
                onClick={handleLogout}
                color="inherit"
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button
                component={RouterLink}
                to="/login"
                color="inherit"
              >
                Login
              </Button>
              <Button
                component={RouterLink}
                to="/register"
                color="inherit"
              >
                Register
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}; 