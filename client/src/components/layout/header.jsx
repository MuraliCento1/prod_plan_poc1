import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { AppBar, Toolbar, IconButton, Typography, Drawer, List, ListItem, ListItemText, useMediaQuery } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import MenuIcon from "@mui/icons-material/Menu";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";

export default function Header() {
  const [darkMode, setDarkMode] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  useEffect(() => {
    if (darkMode) {
      document.body.style.backgroundColor = "#121212";
      document.body.style.color = "#ffffff";
    } else {
      document.body.style.backgroundColor = "#ffffff";
      document.body.style.color = "#000000";
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <AppBar position="sticky" sx={{ background: darkMode ? "#333" : "primary.main" }}>
      <Toolbar>
        <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, textDecoration: "none", color: "inherit", display: "flex",
    alignItems: "center" }}>
          <img src="/logoPlaceholder.png" alt="MyBrand Logo" style={{ height: "80px", width: "auto" }}/>
        </Typography>

        {!isSmallScreen && (
          <Typography component={Link} to="/analytic" sx={{ textDecoration: "none", color: "inherit", marginRight: 2 }}>
            Constrain Analysis
          </Typography>
        )}

        <IconButton onClick={toggleDarkMode} color="inherit">
          {darkMode ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>

        {isSmallScreen && (
          <IconButton onClick={() => setMenuOpen(true)} color="inherit">
            <MenuIcon />
          </IconButton>
        )}
      </Toolbar>

      <Drawer anchor="right" open={menuOpen} onClose={() => setMenuOpen(false)}>
        <List sx={{ width: 250 }}>
          <ListItem button component={Link} to="/analytic" onClick={() => setMenuOpen(false)}>
            <ListItemText primary="Constrain Analysis" />
          </ListItem>
        </List>
      </Drawer>
    </AppBar>
  );
}
