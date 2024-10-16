import type { Location_, ServerErrors } from 'src/client/types';

import axios from "axios";
import { useState, useEffect, useCallback } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Table from '@mui/material/Table';
import Button from '@mui/material/Button';
import TableBody from '@mui/material/TableBody';
import Typography from '@mui/material/Typography';
import TableContainer from '@mui/material/TableContainer';
import TablePagination from '@mui/material/TablePagination';

import { CONFIG } from 'src/config-global';
import { FormErrors } from 'src/client/forms';
import { DashboardContent } from 'src/layouts/dashboard';

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

type LocationServerProps = {
  id: string;
  name: string;
  latitude: string;
  longitude: string;
  is_default: boolean;
  is_active: boolean;
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

  useEffect(() => {
    axios.get(`${CONFIG.api.coreURL}/v1/locations/my`)
    .then(
      (response) => {
	const newLocations = response.data.map(
          ({ id, name, latitude, longitude, is_default, is_active }: LocationServerProps) => {
            const loc: Location_ = {
              id, name, latitude, longitude, isDefault: is_default, isActive: is_active
            };
            return loc;
          }
        );
	setLocations(newLocations);
      }
    )
  }, [refreshCount]);

  const createLocation = () => {
    if (!locations) return;
    setDialogData(nullLocation);
    setDialogCreation(true);
    setDialogOpen(true);
  };

  const editLocation = (locationId: string) => {
    if (!locations) return;
    locations.filter(
      (loc) => loc.id === locationId
    ).forEach((loc) => setDialogData(loc));
    setDialogCreation(false);
    setDialogOpen(true);
  };

  const deleteLocation = (locationId: string) => {
    if (!locations) return;
    axios.delete(`${CONFIG.api.coreURL}/v1/locations/${locationId}`)
    .then(
      () => {
	setRefreshCount(refreshCount + 1);
      }
    );
  };

  const deleteManyLocations = (locationIds: string[]) => {
    locationIds.forEach((locationId) => {
      axios.delete(`${CONFIG.api.coreURL}/v1/locations/${locationId}`)
      .then(
	() => {
	  setRefreshCount(refreshCount + 1);
	}
      );
    });
  }

  const handleDialogSave = () => {
    if (!locations) return;

    const newErrors = new FormErrors();

    if (!dialogData.name) {
      newErrors.addError('name', 'Name is required!');
    }

    if (newErrors.hasErrors()) {
      setDialogErrors(newErrors);
      return;
    }

    const { id, name, latitude, longitude, isDefault, isActive } = dialogData;
    const serverLoc: LocationServerProps = {
      id, name, latitude, longitude, is_default: isDefault, is_active: isActive,
    };

    const req = (isDialogCreation) ? (
      axios.post(
	`${CONFIG.api.coreURL}/v1/locations/`, serverLoc
      )
    ) : (
      axios.put(
	`${CONFIG.api.coreURL}/v1/locations/${id}`, serverLoc
      )
    );
    req.then((result) => {
      setLocations(locations);
      setDialogOpen(false);
      newErrors.clear();
      setDialogErrors(newErrors);
      setRefreshCount(refreshCount + 1);
    })
    .catch(
      (error) => {
	const serverErrors: ServerErrors = error.response.data;
	newErrors.addFromServer(serverErrors);
	setDialogErrors(newErrors);
      }
    );
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
	  onClick={createLocation}
        >
          New location
        </Button>
      </Box>

      <Card>
        <LocationTableToolbar
          numSelected={table.selected.length}
          filterName={filterName}
          onFilterName={(event: React.ChangeEvent<HTMLInputElement>) => {
            setFilterName(event.target.value);
            table.onResetPage();
          }}
	  onDeleteMany={() => deleteManyLocations(table.selected)}
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
                    { id: 'isDefault', label: 'Default', align: 'center' },
                    { id: 'isActive', label: 'Active', align: 'center' },
                    { id: '' },
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
                        handleEdit={() => editLocation(row.id)}
                        handleDelete={() => deleteLocation(row.id)}
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
