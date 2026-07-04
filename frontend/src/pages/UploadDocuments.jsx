import { useState } from "react";

import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";

import UploadDropzone from "../components/upload/UploadDropzone";
import UploadedDocuments from "../components/upload/UploadedDocuments";

import { useTheme } from "../context/ThemeContext";
import { authFetch } from "../services/api";

function UploadDocuments() {
  const { darkMode } = useTheme();

  const [files, setFiles] = useState([
    {
      id: 1,
      type: "PDF",
      name: "Anderson_Corp_Evidence_Pack.pdf",
      size: "4.2 MB",
      time: "2 hours ago",
      status: "Ready",
    },
    {
      id: 2,
      type: "DOCX",
      name: "Blackwell_Testimony_Transcript.docx",
      size: "1.8 MB",
      time: "5 hours ago",
      status: "Ready",
    },
    {
      id: 3,
      type: "PDF",
      name: "Mercer_Patent_Filing_2024.pdf",
      size: "8.6 MB",
      time: "Just now",
      status: "Analyzing",
      progress: 72,
    },
    {
      id: 4,
      type: "PDF",
      name: "Rivera_Settlement_Draft.pdf",
      size: "2.1 MB",
      time: "Yesterday",
      status: "Ready",
    },
    {
      id: 5,
      type: "PDF",
      name: "Greenfield_Will_Contested.pdf",
      size: "3.4 MB",
      time: "Yesterday",
      status: "Ready",
    },
  ]);

  // Handle uploaded files
  const handleFilesUpload = async (selectedFiles) => {
    const uploadedFiles = Array.from(selectedFiles).map((file) => ({
      id: Date.now().toString() + Math.random().toString(36).substring(7),
      type: file.name.split(".").pop().toUpperCase(),
      name: file.name,
      size: `${(file.size / (1024 * 1024)).toFixed(2)} MB`,
      time: "Just now",
      status: "Uploading",
      progress: 0,
    }));

    setFiles((prev) => [...uploadedFiles, ...prev]);

    for (let i = 0; i < selectedFiles.length; i++) {
      const file = selectedFiles[i];
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await authFetch("/api/v1/documents/upload", {
          method: "POST",
          body: formData,
        });
        
        if (response.ok) {
          setFiles((prev) => 
            prev.map(f => f.name === file.name ? { ...f, status: "Analyzing" } : f)
          );
        } else {
          setFiles((prev) => 
            prev.map(f => f.name === file.name ? { ...f, status: "Failed" } : f)
          );
        }
      } catch (error) {
        console.error("Upload error:", error);
        setFiles((prev) => 
          prev.map(f => f.name === file.name ? { ...f, status: "Failed" } : f)
        );
      }
    }
  };

  return (
    <div
      className={`min-h-screen flex transition-all duration-300 ${
        darkMode ? "bg-slate-900" : "bg-slate-50"
      }`}
    >
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 overflow-auto p-8">
        {/* Navbar */}
        <Navbar />

        {/* Header */}
        <div className="mt-8">
          <h1
            className={`text-4xl font-bold ${
              darkMode ? "text-white" : "text-slate-900"
            }`}
          >
            Document Upload
          </h1>

          <p
            className={`mt-2 text-lg ${
              darkMode ? "text-slate-400" : "text-slate-500"
            }`}
          >
            Upload legal documents for AI-powered analysis
          </p>
        </div>

        {/* Upload Area */}
        <div className="mt-10">
          <UploadDropzone onUpload={handleFilesUpload} />
        </div>

        {/* Uploaded Documents */}
        <div className="mt-10">
          <UploadedDocuments files={files} />
        </div>
      </div>
    </div>
  );
}

export default UploadDocuments;