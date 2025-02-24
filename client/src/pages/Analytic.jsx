import React from "react";
import "../styles/Analytic.css";

const Analytic = () => {
  return (
    <div className="analytic-container">
      <div className="left-section">
        <div className="table-container table-one">
          <h2>Parent SKU Details</h2>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Parent</th>
                <th>Sku Code</th>
                <th>Planned Qty</th>
                <th>Feasible Qty</th>
                <th>Unfeasible Qty</th>
              </tr>
            </thead>
            <tbody>
              
            </tbody>
          </table>
        </div>
      </div>

      <div className="right-section">
        {/* Upper Table */}
        <div className="table-container table-two">
          <h2>Child SKU Details</h2>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Child Sku Code</th>
                <th>Bom Qty</th>
                <th>Alloted Qty</th>
                <th>Attributed FG prod</th>
                <th>Opening Stock</th>
                <th>Total Available Qty</th>
              </tr>
            </thead>
            <tbody>
              
            </tbody>
          </table>
        </div>

        {/* Lower Table */}
        <div className="table-container table-three">
          <h2>Machine Capacity</h2>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Machine Code</th>
                <th>Alloted Machine Capacity</th>
                <th>Required MC Cap</th>
                <th>Total Req MC Cap</th>
                <th>Throughput</th>
                <th>Available MC Capacity</th>
              </tr>
            </thead>
            <tbody>
              
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Analytic;
