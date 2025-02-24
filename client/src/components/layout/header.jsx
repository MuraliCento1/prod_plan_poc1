import { useState } from "react";
import { Link } from "react-router-dom";

export default function Header() {
  const [darkMode, setDarkMode] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle("dark-mode");
  };

  return (
    <header className={`header ${darkMode ? "dark" : ""}`}>
      <Link to="/" className="logo">
        <img src="/logoPlaceholder.png" alt="MyBrand Logo" style={{height: '150%'}} />
    </Link>


      <nav className={`nav-links ${menuOpen ? "open" : ""}`}>
        <Link to="/analytic">Analytic</Link>
      </nav>

      <div className="header-icons">
        <button onClick={toggleDarkMode} className="toggle-theme">
          {darkMode ? "🌞" : "🌙"}
        </button>
        <button onClick={() => setMenuOpen(!menuOpen)} className="menu-toggle">
          ☰
        </button>
      </div>
    </header>
  );
}
