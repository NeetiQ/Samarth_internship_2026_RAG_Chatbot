const UploadStats = () => {
  const cardStyle = {
    flex: 1,
    background: "white",
    padding: "16px",
    borderRadius: "12px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.06)",
    textAlign: "center",
  };

  return (
    <div style={{ display: "flex", gap: "15px" }}>
      <div style={cardStyle}>
        <h3 style={{ margin: 0 }}>0</h3>
        <p style={{ margin: 0, color: "#777" }}>Total Files</p>
      </div>

      <div style={cardStyle}>
        <h3 style={{ margin: 0 }}>0</h3>
        <p style={{ margin: 0, color: "#777" }}>Processing</p>
      </div>

      <div style={cardStyle}>
        <h3 style={{ margin: 0 }}>0</h3>
        <p style={{ margin: 0, color: "#777" }}>Completed</p>
      </div>
    </div>
  );
};

export default UploadStats;