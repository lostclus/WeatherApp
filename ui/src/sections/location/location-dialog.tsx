import type { ChangeEvent } from 'react';
import type { FormErrors } from 'src/client/forms';
import type { Location_ } from 'src/client/locations';

import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import Switch from '@mui/material/Switch';
import TextField from '@mui/material/TextField';
import DialogTitle from '@mui/material/DialogTitle';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import FormControlLabel from '@mui/material/FormControlLabel';


export interface LocationDialogProps {
  open: boolean;
  isCreation: boolean;
  formData: Location_,
  setFormData: (newData: Location_) => void,
  errors: FormErrors,
  onClose: () => void;
  onSave: () => void;
}

export function LocationDialog(props: LocationDialogProps) {
  const {
    open,
    isCreation,
    formData,
    setFormData,
    errors,
    onClose,
    onSave
  } = props;

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value, checked } = event.target;
    let newValue: string | boolean = value;
    if (name === "isDefault" || name === "isActive")
      newValue = checked;
    const newData = { ...formData, [name]: newValue } as Location_;
    setFormData(newData);
  };

  return (
    <Dialog fullWidth onClose={onClose} open={open}>
      <DialogTitle>{(isCreation) ? "New location" : "Edit location"}</DialogTitle>
      <DialogContent>
	<Stack spacing={2}>
	  <TextField
	    required
	    margin="dense"
	    id="name"
	    name="name"
	    label="Location name"
	    fullWidth
	    variant="standard"
	    value={formData.name}
	    onChange={handleChange}
	    error={errors.hasErrorsIn('name', '__all__')}
	    helperText={errors.getErrorsIn('name', '__all__')}
	  />
	  <TextField
	    required
	    margin="dense"
	    id="latitude"
	    name="latitude"
	    label="Latitude"
	    fullWidth
	    variant="standard"
	    type="number"
	    value={formData.latitude}
	    onChange={handleChange}
	    error={errors.hasErrorsIn('latitude')}
	    helperText={errors.getErrorsIn('latitude')}
	  />
	  <TextField
	    required
	    margin="dense"
	    id="longitude"
	    name="longitude"
	    label="Longitude"
	    fullWidth
	    variant="standard"
	    type="number"
	    value={formData.longitude}
	    onChange={handleChange}
	    error={errors.hasErrorsIn('longitude')}
	    helperText={errors.getErrorsIn('longitude')}
	  />
	  <FormControlLabel
	    label="Default"
	    control={(
	      <Switch
		name="isDefault"
		checked={formData.isDefault}
		onChange={handleChange}
	      />
	    )}
	  />
	  <FormControlLabel
	    label="Active"
	    control={(
	      <Switch
		name="isActive"
		checked={formData.isActive}
		onChange={handleChange}
	       />
	    )}
	  />
	</Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button type="submit" onClick={onSave}>Save</Button>
      </DialogActions>
    </Dialog>
  );
}
