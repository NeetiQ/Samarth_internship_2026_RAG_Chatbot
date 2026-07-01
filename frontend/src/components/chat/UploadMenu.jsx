import { motion } from "framer-motion";
import { FiFileText, FiImage, FiFolder } from "react-icons/fi";
import { useTheme } from "../../context/ThemeContext";

function UploadMenu({
  onPdfUpload,
  onImageUpload,
  onCaseUpload,
}) {
  const { darkMode } = useTheme();

  const options = [
    {
      icon: <FiFileText />,
      title: "PDF Document",
      onClick: onPdfUpload,
    },
    {
      icon: <FiImage />,
      title: "Evidence Image",
      onClick: onImageUpload,
    },
    {
      icon: <FiFolder />,
      title: "Case Files",
      onClick: onCaseUpload,
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`absolute bottom-16 left-0 w-64 rounded-2xl border p-3 z-50 ${
        darkMode
          ? "bg-[#111827] border-[#1E293B]"
          : "bg-white border-slate-200"
      }`}
    >
      {options.map((item, index) => (
        <button
          key={index}
          onClick={item.onClick}
          className={`w-full flex items-center gap-3 p-3 rounded-xl transition ${
            darkMode
              ? "hover:bg-[#1A2333]"
              : "hover:bg-slate-50"
          }`}
        >
          <div className="text-[#2348C6] text-lg">
            {item.icon}
          </div>

          <span
            className={`font-medium ${
              darkMode
                ? "text-slate-200"
                : "text-slate-700"
            }`}
          >
            {item.title}
          </span>
        </button>
      ))}
    </motion.div>
  );
}

export default UploadMenu;