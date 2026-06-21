import { FiBell, FiSearch } from "react-icons/fi";

function Navbar() {
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

        <div className="w-12 h-12 rounded-full bg-[#2348C6] text-white flex items-center justify-center font-bold">
          NAI
        </div>
      </div>

    </div>
  );
}

export default Navbar;