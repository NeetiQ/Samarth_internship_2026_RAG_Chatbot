import {
  FiFileText,
  FiCheckCircle,
  FiLoader,
  FiUpload,
} from "react-icons/fi";

import { useTheme } from "../../context/ThemeContext";

function UploadedDocuments({ files }) {
  const { darkMode } = useTheme();

  const getTypeColor = (type) => {
    switch (type) {
      case "PDF":
        return "bg-red-100 text-red-600";
      case "DOCX":
        return "bg-blue-100 text-blue-600";
      case "TXT":
        return "bg-green-100 text-green-600";
      case "XLSX":
        return "bg-emerald-100 text-emerald-600";
      default:
        return "bg-slate-100 text-slate-600";
    }
  };

  return (
    <div
      className={`mt-10 rounded-3xl shadow-lg overflow-hidden transition-all duration-300 ${
        darkMode ? "bg-slate-800" : "bg-white"
      }`}
    >
      {/* Header */}

      <div
        className={`flex items-center justify-between px-8 py-6 border-b ${
          darkMode ? "border-slate-700" : "border-slate-200"
        }`}
      >
        <div>
          <h2
            className={`text-2xl font-bold ${
              darkMode ? "text-white" : "text-slate-900"
            }`}
          >
            Uploaded Documents
          </h2>

          <p
            className={`text-sm mt-1 ${
              darkMode ? "text-slate-400" : "text-slate-500"
            }`}
          >
            Documents ready for AI retrieval
          </p>
        </div>

        <div
          className={`px-4 py-2 rounded-xl text-sm font-semibold ${
            darkMode
              ? "bg-slate-700 text-white"
              : "bg-slate-100 text-slate-700"
          }`}
        >
          {files.length} Files
        </div>
      </div>

      {/* Empty */}

      {files.length === 0 && (
        <div className="py-20 text-center">
          <FiFileText
            size={60}
            className="mx-auto text-slate-400"
          />

          <h3
            className={`mt-5 text-xl font-semibold ${
              darkMode ? "text-white" : "text-slate-800"
            }`}
          >
            No Documents Uploaded
          </h3>

          <p
            className={`mt-3 ${
              darkMode ? "text-slate-400" : "text-slate-500"
            }`}
          >
            Upload PDFs, DOCX, TXT or XLSX files to begin AI analysis.
          </p>
        </div>
      )}

      {/* Files */}

      {files.length > 0 && (
        <div className="divide-y divide-slate-200 dark:divide-slate-700">

          {files.map((file) => (
            <div
              key={file.id}
              className={`flex justify-between items-center px-8 py-6 transition hover:${
                darkMode ? "bg-slate-700" : "bg-slate-50"
              }`}
            >
              {/* Left */}

              <div className="flex items-center gap-5">

                <div
                  className={`w-14 h-14 rounded-xl flex items-center justify-center font-bold ${getTypeColor(
                    file.type
                  )}`}
                >
                  {file.type}
                </div>

                <div>

                  <h3
                    className={`font-semibold text-lg ${
                      darkMode ? "text-white" : "text-slate-900"
                    }`}
                  >
                    {file.name}
                  </h3>

                  <p
                    className={`text-sm mt-1 ${
                      darkMode ? "text-slate-400" : "text-slate-500"
                    }`}
                  >
                    {file.size} • {file.time}
                  </p>

                  {/* Upload Progress */}

                  {file.status === "Uploading" && (
                    <div className="mt-4 w-72">

                      <div className="flex justify-between text-xs mb-2">
                        <span className="text-blue-500">
                          Uploading...
                        </span>

                        <span>{file.progress}%</span>
                      </div>

                      <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-blue-600 transition-all duration-500"
                          style={{
                            width: `${file.progress}%`,
                          }}
                        />
                      </div>

                    </div>
                  )}

                  {/* AI Progress */}

                  {file.status === "Analyzing" && (
                    <div className="mt-4 w-72">

                      <div className="flex justify-between text-xs mb-2">
                        <span className="text-yellow-500">
                          AI Processing...
                        </span>

                        <span>{file.progress}%</span>
                      </div>

                      <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-yellow-500 transition-all duration-500"
                          style={{
                            width: `${file.progress}%`,
                          }}
                        />
                      </div>

                    </div>
                  )}

                </div>

              </div>

              {/* Status */}

              <div>

                {file.status === "Uploading" && (
                  <div className="flex items-center gap-2 text-blue-600 font-medium">
                    <FiUpload />
                    Uploading
                  </div>
                )}

                {file.status === "Analyzing" && (
                  <div className="flex items-center gap-2 text-yellow-500 font-medium">
                    <FiLoader className="animate-spin" />
                    AI Analyzing
                  </div>
                )}

                {file.status === "Ready" && (
                  <div className="flex items-center gap-2 text-green-600 font-semibold">
                    <FiCheckCircle />
                    Ready
                  </div>
                )}

              </div>

            </div>
          ))}

        </div>
      )}
    </div>
  );
}

export default UploadedDocuments;