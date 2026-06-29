import { FiUploadCloud } from "react-icons/fi";
import { useRef } from "react";
import { useTheme } from "../../context/ThemeContext";

function UploadDropzone({ onUpload }) {
  const inputRef = useRef();
  const { darkMode } = useTheme();

  const handleFiles = (files) => {
    if (!files || files.length === 0) return;

    onUpload(files);
  };

  return (
    <>
      <input
        ref={inputRef}
        hidden
        multiple
        type="file"
        accept=".pdf,.doc,.docx,.txt,.xlsx"
        onChange={(e) => handleFiles(e.target.files)}
      />

      <div
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          handleFiles(e.dataTransfer.files);
        }}
        className={`cursor-pointer rounded-3xl border-2 border-dashed p-14 transition-all duration-300
        ${
          darkMode
            ? "bg-slate-800 border-slate-700 hover:border-blue-500"
            : "bg-white border-slate-300 hover:border-blue-500"
        }`}
      >
        <div className="flex flex-col items-center">

          <div
            className={`w-24 h-24 rounded-full flex items-center justify-center ${
              darkMode ? "bg-slate-700" : "bg-blue-50"
            }`}
          >
            <FiUploadCloud
              size={55}
              className="text-blue-600"
            />
          </div>

          <h2
            className={`mt-8 text-2xl font-bold ${
              darkMode ? "text-white" : "text-slate-900"
            }`}
          >
            Drag & Drop files here
          </h2>

          <p
            className={`mt-3 ${
              darkMode ? "text-slate-400" : "text-slate-500"
            }`}
          >
            or click to browse
          </p>

          <p
            className={`mt-2 ${
              darkMode ? "text-slate-500" : "text-slate-400"
            }`}
          >
            PDF • DOCX • TXT • XLSX supported
          </p>

          <button className="mt-8 bg-blue-600 hover:bg-blue-700 text-white px-7 py-3 rounded-xl font-semibold transition">
            Browse Files
          </button>
        </div>
      </div>

      <div className="flex gap-4 mt-6">
        <span className="px-4 py-2 rounded-xl bg-green-500 text-white">
          🔐 E2E Encrypted
        </span>

        <span className="px-4 py-2 rounded-xl bg-indigo-600 text-white">
          ⚖ Privilege Protected
        </span>

        <span className="px-4 py-2 rounded-xl bg-blue-600 text-white">
          🤖 AI Analysis
        </span>
      </div>
    </>
  );
}

export default UploadDropzone;