import { FiBell, FiSearch, FiMoon, FiSun } from "react-icons/fi";
import { useTheme } from "../../context/ThemeContext";

function Navbar() {
  const { darkMode, setDarkMode } = useTheme();

  return (
    <div className="flex justify-between items-center">

      <div className="bg-white rounded-2xl shadow px-5 py-3 flex items-center gap-3 w-[500px]">
        <FiSearch />

        <input
          className="outline-none w-full"
          placeholder="Search cases, documents, precedents..."
        />
      </div>

      <div className="flex items-center gap-5">

        <FiBell size={22} />

        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 rounded-full hover:bg-gray-100 transition"
        >
          {darkMode ? (
            <FiSun size={22} />
          ) : (
            <FiMoon size={22} />
          )}
        </button>

        <div className="w-12 h-12 rounded-full bg-[#2348C6] text-white flex items-center justify-center font-bold">
          NAI
        </div>

      </div>
    </div>
  );
}

export default Navbar;