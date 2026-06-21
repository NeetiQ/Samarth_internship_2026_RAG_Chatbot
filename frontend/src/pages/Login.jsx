export default function Login() {
  return (
    <div className="min-h-screen flex">

      {/* Left Section */}
      <div className="hidden lg:flex w-1/2 bg-slate-800 text-white flex-col justify-center items-center">

        <div className="text-center">

          <h1 className="text-6xl font-bold">
            ⚖️ NyayaAI
          </h1>

          <p className="text-slate-300 mt-4 text-xl">
            Justice Meets Intelligence
          </p>

        </div>

      </div>

      {/* Right Section */}
      <div className="w-full lg:w-1/2 flex justify-center items-center bg-slate-50">

        <div className="bg-white p-10 rounded-3xl shadow-xl w-[420px]">

          <h2 className="text-3xl font-bold text-slate-800">
            Sign In
          </h2>

          <p className="text-gray-500 mt-2 mb-6">
            Welcome back
          </p>

          <input
            type="email"
            placeholder="Email"
            className="w-full border rounded-xl p-3 mb-4"
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full border rounded-xl p-3 mb-6"
          />

          <button
            className="w-full bg-blue-600 text-white py-3 rounded-xl"
          >
            Continue
          </button>

        </div>

      </div>

    </div>
  );
}