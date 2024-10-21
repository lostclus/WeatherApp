import type { ServerErrors } from 'src/client/types';
import type { Location_ } from 'src/client/locations';

import { useState, useEffect, useCallback } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Table from '@mui/material/Table';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import TableBody from '@mui/material/TableBody';
import Typography from '@mui/material/Typography';
import TableContainer from '@mui/material/TableContainer';
import TablePagination from '@mui/material/TablePagination';

import { FormErrors } from 'src/client/forms';
import { DashboardContent } from 'src/layouts/dashboard';
import { createLocation, updateLocation, deleteLocation, getMyLocations } from 'src/client/locations';

import { Iconify } from 'src/components/iconify';
import { Scrollbar } from 'src/components/scrollbar';

import { TableNoData } from '../table-no-data';
import { LocationDialog } from '../location-dialog';
import { TableEmptyRows } from '../table-empty-rows';
import { LocationTableRow } from '../location-table-row';
import { LocationTableHead } from '../location-table-head';
import { LocationTableToolbar } from '../location-table-toolbar';
import { emptyRows, applyFilter, getComparator } from '../utils';

const nullLocation: Location_ = {
    id: "",
    name: "",
    latitude: "",
    longitude: "",
    isDefault: false,
    isActive: true,
};

// ----------------------------------------------------------------------

export function LocationsView() {
  const table = useTable();

  const [filterName, setFilterName] = useState('');
  const [locations, setLocations] = useState<Location_[] | null>(null);
  const [isDialogOpen, setDialogOpen] = useState(false);
  const [isDialogCreation, setDialogCreation] = useState(false);
  const [dialogData, setDialogData] = useState(nullLocation);
  const [dialogErrors, setDialogErrors] = useState(new FormErrors());
  const [refreshCount, setRefreshCount] = useState(0);
  const [successMsg, setSuccessMsg] = useState("");

  useEffect(() => {
    getMyLocations((newLocations) => setLocations(newLocations));
  }, [refreshCount]);

  const handleAddLocation = () => {
    if (!locations) return;
    setDialogData(nullLocation);
    setDialogCreation(true);
    setDialogOpen(true);
    setSuccessMsg("");
  };

  const handleEditLocation = (locationId: string) => {
    if (!locations) return;
    locations.filter(
      (loc) => loc.id === locationId
    ).forEach((loc) => setDialogData(loc));
    setDialogCreation(false);
    setDialogOpen(true);
    setSuccessMsg("");
  };

  const handleDeleteLocation = (locationId: string) => {
    if (!locations) return;
    deleteLocation(locationId, () => {
      setRefreshCount(refreshCount + 1);
      setSuccessMsg("Location was deleted.");
    });
  };

  const handleDeleteManyLocations = (locationIds: string[]) => {
    locationIds.forEach((locationId) => {
      deleteLocation(locationId, () => {
	setRefreshCount(refreshCount + 1);
	setSuccessMsg("Location was deleted.");
      });
    });
  }

  const handleDialogSave = () => {
    if (!locations) return;

    const newErrors = new FormErrors();

    setSuccessMsg("");

    if (!dialogData.name) {
      newErrors.addError('name', 'Name is required!');
    }

    if (newErrors.hasErrors()) {
      setDialogErrors(newErrors);
      return;
    }

    const onSuccess = (loc: Location_) => {
      setDialogOpen(false);
      newErrors.clear();
      setDialogErrors(newErrors);
      setRefreshCount(refreshCount + 1);
      setSuccessMsg((isDialogCreation) ? "Location was created." : "Location was updated.");
    };

    const onError = (serverErrors: ServerErrors) => {
      newErrors.addFromServer(serverErrors);
      setDialogErrors(newErrors);
    }

    if (isDialogCreation) {
      createLocation(
	dialogData,
	onSuccess,
	onError,
      );
    } else {
      updateLocation(
	dialogData,
	onSuccess,
	onError,
      );
    }
  }

  const dataFiltered: Location_[] = applyFilter({
    inputData: locations || [],
    comparator: getComparator(table.order, table.orderBy),
    filterName,
  });

  const notFound = !dataFiltered.length && !!filterName;

  return (
    <DashboardContent>
      <Box display="flex" alignItems="center" mb={5}>
        <Typography variant="h4" flexGrow={1}>
          Locations
        </Typography>
        <Button
          variant="contained"
          color="inherit"
          startIcon={<Iconify icon="mingcute:add-line" />}
	  onClick={handleAddLocation}
        >
          New location
        </Button>
      </Box>

      <Snackbar
	open={Boolean(successMsg)}
	anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
	autoHideDuration={3000}
	onClose={() => setSuccessMsg("")}
      >
	<Alert severity="success" variant="filled">{successMsg}</Alert>
      </Snackbar>

      <Card>
        <LocationTableToolbar
          numSelected={table.selected.length}
          filterName={filterName}
          onFilterName={(event: React.ChangeEvent<HTMLInputElement>) => {
            setFilterName(event.target.value);
            table.onResetPage();
          }}
	  onDeleteMany={() => handleDeleteManyLocations(table.selected)}
        />

        <Scrollbar>
          {(locations === null) ? "" : (
            <TableContainer sx={{ overflow: 'unset' }}>
              <Table sx={{ minWidth: 800 }}>
                <LocationTableHead
                  order={table.order}
                  orderBy={table.orderBy}
                  rowCount={locations.length}
                  numSelected={table.selected.length}
                  onSort={table.onSort}
                  onSelectAllRows={(checked) =>
                    table.onSelectAllRows(
                      checked,
                      locations.map((loc) => loc.id)
                    )
                  }
                  headLabel={[
                    { id: 'name', label: 'Name' },
                    { id: 'isDefault', label: 'Default', align: 'center', width: 50 },
                    { id: 'isActive', label: 'Active', align: 'center', width: 50 },
                    { id: '', width: 50 },
                  ]}
                />
                <TableBody>
                  {dataFiltered
                    .slice(
                      table.page * table.rowsPerPage,
                      table.page * table.rowsPerPage + table.rowsPerPage
                    )
                    .map((row) => (
                      <LocationTableRow
                        key={row.id}
                        row={row}
                        selected={table.selected.includes(row.id)}
                        onSelectRow={() => table.onSelectRow(row.id)}
                        handleEdit={() => handleEditLocation(row.id)}
                        handleDelete={() => handleDeleteLocation(row.id)}
                      />
                    ))}

                  <TableEmptyRows
                    height={68}
                    emptyRows={emptyRows(table.page, table.rowsPerPage, locations.length)}
                  />

                  {notFound && <TableNoData searchQuery={filterName} />}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Scrollbar>

        <TablePagination
          component="div"
          page={table.page}
          count={(locations) ? locations.length : 0}
          rowsPerPage={table.rowsPerPage}
          onPageChange={table.onChangePage}
          rowsPerPageOptions={[10, 25, 100]}
          onRowsPerPageChange={table.onChangeRowsPerPage}
        />
      </Card>
      <LocationDialog
        open={isDialogOpen}
        isCreation={isDialogCreation}
        formData={dialogData}
        setFormData={setDialogData}
	errors={dialogErrors}
        onClose={() => setDialogOpen(false)}
        onSave={handleDialogSave}
      />
    </DashboardContent>
  );
}

// ----------------------------------------------------------------------

export function useTable() {
  const [page, setPage] = useState(0);
  const [orderBy, setOrderBy] = useState('name');
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selected, setSelected] = useState<string[]>([]);
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');

  const onSort = useCallback(
    (id: string) => {
      const isAsc = orderBy === id && order === 'asc';
      setOrder(isAsc ? 'desc' : 'asc');
      setOrderBy(id);
    },
    [order, orderBy]
  );

  const onSelectAllRows = useCallback((checked: boolean, newSelecteds: string[]) => {
    if (checked) {
      setSelected(newSelecteds);
      return;
    }
    setSelected([]);
  }, []);

  const onSelectRow = useCallback(
    (inputValue: string) => {
      const newSelected = selected.includes(inputValue)
        ? selected.filter((value) => value !== inputValue)
        : [...selected, inputValue];

      setSelected(newSelected);
    },
    [selected]
  );

  const onResetPage = useCallback(() => {
    setPage(0);
  }, []);

  const onChangePage = useCallback((event: unknown, newPage: number) => {
    setPage(newPage);
  }, []);

  const onChangeRowsPerPage = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setRowsPerPage(parseInt(event.target.value, 10));
      onResetPage();
    },
    [onResetPage]
  );

  return {
    page,
    order,
    onSort,
    orderBy,
    selected,
    rowsPerPage,
    onSelectRow,
    onResetPage,
    onChangePage,
    onSelectAllRows,
    onChangeRowsPerPage,
  };
}
