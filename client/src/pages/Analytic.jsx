import React, { useEffect, useState } from "react";
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, useMediaQuery } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import axios from "axios";

const Analytic = () => {
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("md"));
  const baseUrl = process.env.REACT_APP_BASE_URL;

  const [fgData, setFgData] = useState([]);
  const [rmData, setRmData] = useState([]);
  const [machineData, setMachineData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const fgResponse = await axios.get(`${baseUrl}/get-fg-data/?plant_code=1&FG=string1&machine=string2`);
        setFgData(fgResponse.data);
        
        const rmResponse = await axios.get(`${baseUrl}/get-rm-data/?plant_code=1&FG=string01&FG=string02&rm=mm2&rm=mm3`);
        setRmData(rmResponse.data);

        const machineResponse = await axios.get(`${baseUrl}/get-machine-data/?plant_code=1&rm=rm2&rm=rm2&machine=mmm3&machine=m12`);
        setMachineData(machineResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [baseUrl]);

  return (
    <Box display="flex" flexDirection={isSmallScreen ? "column" : "row"} gap={2} p={2} height="calc(100vh - 64px)">
      {/* Left Section - FG TABLE Details */}
      <Box flex={0.4} component={Paper} p={2} sx={{ overflow: "hidden", height: isSmallScreen ? "auto" : "100%" }}>
        <Typography variant="h6" sx={{ bgcolor: "#E3F2FD", p: 1, borderRadius: 1 }}>FG TABLE</Typography>
        <TableContainer sx={{ maxHeight: "calc(100% - 50px)" }}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell>Parent</TableCell>
                <TableCell>Planned Qty</TableCell>
                <TableCell>Feasible Qty</TableCell>
                <TableCell>Unfeasible Qty</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {fgData.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>{row.date}</TableCell>
                  <TableCell>{row.parent}</TableCell>
                  <TableCell>{row.planned_qty}</TableCell>
                  <TableCell>{row.feasible_qty}</TableCell>
                  <TableCell>{row.unfeasible_qty}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>

      {/* Right Section */}
      <Box flex={0.6} display="flex" flexDirection="column" gap={2}>
        {/* RM table */}
        <Box component={Paper} p={2} sx={{ overflow: "hidden", height: isSmallScreen ? "auto" : "50%" }}>
          <Typography variant="h6" sx={{ bgcolor: "#E8F5E9", p: 1, borderRadius: 1 }}>RM TABLE</Typography>
          <TableContainer sx={{ maxHeight: "calc(100% - 50px)" }}>
            <Table stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell>Date</TableCell>
                  <TableCell>Child Sku Code</TableCell>
                  <TableCell>Bom Qty</TableCell>
                  <TableCell>Net Requirement</TableCell>
                  <TableCell>Alloted Qty</TableCell>
                  <TableCell>Attributed FG prod loss</TableCell>
                  <TableCell>Opening Stock</TableCell>
                  <TableCell>Inwarding stock</TableCell>
                  <TableCell>Total Available Qty</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rmData.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell>{row.date}</TableCell>
                    <TableCell>{row.child_sku_code}</TableCell>
                    <TableCell>{row.bom_qty}</TableCell>
                    <TableCell>{row.net_requirement}</TableCell>
                    <TableCell>{row.alloted_qty}</TableCell>
                    <TableCell>{row.attributed_fg_prod_loss}</TableCell>
                    <TableCell>{row.opening_stock}</TableCell>
                    <TableCell>{row.inwarding_stock}</TableCell>
                    <TableCell>{row.total_available_qty}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>

        {/* Machine table */}
        <Box component={Paper} p={2} sx={{ overflow: "hidden", height: isSmallScreen ? "auto" : "50%" }}>
          <Typography variant="h6" sx={{ bgcolor: "#FFF3E0", p: 1, borderRadius: 1 }}>MACHINE TABLE</Typography>
          <TableContainer sx={{ maxHeight: "calc(100% - 50px)" }}>
            <Table stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell>Date</TableCell>
                  <TableCell>Machine Code</TableCell>
                  <TableCell>Alloted Machine Capacity</TableCell>
                  <TableCell>Required MC Cap</TableCell>
                  <TableCell>Total Req MC Cap</TableCell>
                  <TableCell>Throughput</TableCell>
                  <TableCell>Available MC Capacity</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {machineData.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell>{row.date}</TableCell>
                    <TableCell>{row.machine_code}</TableCell>
                    <TableCell>{row.alloted_machine_capacity}</TableCell>
                    <TableCell>{row.required_mc_cap}</TableCell>
                    <TableCell>{row.total_req_mc_cap}</TableCell>
                    <TableCell>{row.throughput}</TableCell>
                    <TableCell>{row.available_mc_capacity}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      </Box>
    </Box>
  );
};

export default Analytic;
