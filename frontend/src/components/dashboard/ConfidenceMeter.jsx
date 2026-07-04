function ConfidenceMeter() {
  return (
    <div className="bg-white rounded-3xl p-6 shadow-md">
      <h2 className="text-xl font-bold mb-5">
        AI Confidence
      </h2>

      <div className="flex items-center justify-center h-[150px]">
        <p className="text-5xl font-bold text-gray-300">
          --
        </p>
      </div>

      <p className="text-center text-gray-400">
        Waiting for AI data
      </p>
    </div>
  );
}

export default ConfidenceMeter;