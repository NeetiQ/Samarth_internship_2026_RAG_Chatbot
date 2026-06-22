import { FiHome, FiMessageSquare, FiUpload, FiSettings } from "react-icons/fi";

function Sidebar() {
  return (
    <div className="w-72 bg-white border-r border-gray-200 p-6">
      <h1 className="text-4xl font-bold text-[#1E3A8A]">
        ⚖️ NyayaAI
      </h1>

      <p className="text-gray-500 mt-2">
        Justice Meets Intelligence
      </p>

      <div className="mt-12 space-y-6">

        <div className="flex items-center gap-3 text-[#2348C6] font-semibold">
          <FiHome />
          Dashboard
        </div>

        <div className="flex items-center gap-3 text-gray-500">
          <FiMessageSquare />
          Chat Assistant
        </div>

        <div className="flex items-center gap-3 text-gray-500">
          <FiUpload />
          Upload Documents
        </div>

        <div className="flex items-center gap-3 text-gray-500">
          <FiSettings />
          Settings
        </div>

      </div>
    </div>
  );
}

export default Sidebar;