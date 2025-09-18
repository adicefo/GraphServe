import { Component, OnInit } from '@angular/core';
import { MasterComponent } from '../master/master.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DriverService } from '../../services/driver.service';
import { Driver } from '../../models/driver';
import { FormControl, FormGroup, Validators, ReactiveFormsModule, ValidatorFn, AbstractControlOptions } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { SearchResult } from '../../models/search_result';

@Component({
  selector: 'app-driver',
  standalone: true,
  imports: [MasterComponent, CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './driver.component.html',
  styleUrl: './driver.component.css'
})
export class DriverComponent implements OnInit {
  drivers: SearchResult<Driver> = {
    result: [],
    count: 0
  };
  filteredDrivers: Driver[] = [];
  isLoading: boolean = false;
  error: string | null = null;

  nameFilter = new FormControl('');
  surnameFilter = new FormControl('');

  selectedDriver: Driver | null = null;
  driverToDelete: Driver | null = null;
  addDriverModal: boolean = false;
  showDeleteConfirmation = false;
  viewMode: 'grid' | 'list' = 'grid';

  // Form for adding new driver
  driverForm: FormGroup;
  formSubmitted = false;
  formErrors: any = {};

  constructor(private driverService: DriverService) {
    this.driverForm = new FormGroup({
      name: new FormControl('', [Validators.required]),
      surname: new FormControl('', [Validators.required]),
      username: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required]),
      password_confirm: new FormControl('', [Validators.required]),
      telephone_number: new FormControl('', [Validators.required]),
      gender: new FormControl('', [Validators.required]),
      active: new FormControl(true)
    }, { validators: DriverComponent.passwordMatchValidator } as AbstractControlOptions);
  }

  ngOnInit(): void {
    this.loadDrivers();

    // Setup filters
    this.nameFilter.valueChanges
      .pipe(
        debounceTime(300),
        distinctUntilChanged()
      )
      .subscribe(() => this.applyFilters());

    this.surnameFilter.valueChanges
      .pipe(
        debounceTime(300),
        distinctUntilChanged()
      )
      .subscribe(() => this.applyFilters());
  }

  loadDrivers(): void {
    this.isLoading = true;
    this.error = null;

    this.driverService.getAll().subscribe({
      next: (data: SearchResult<Driver>) => {
        this.drivers = data;
        this.filteredDrivers = data.result || [];
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Failed to load drivers. Please try again later.';
        this.isLoading = false;
        console.error('Error loading drivers:', err);
      }
    });
  }

  applyFilters(): void {
    const nameValue = this.nameFilter.value?.toLowerCase() || '';
    const surnameValue = this.surnameFilter.value?.toLowerCase() || '';

    this.filteredDrivers = this.drivers.result?.filter(driver => {
      const matchesName = !nameValue ||
        (driver.user?.name?.toLowerCase().includes(nameValue));
      const matchesSurname = !surnameValue ||
        (driver.user?.surname?.toLowerCase().includes(surnameValue));

      return matchesName && matchesSurname;
    }) || [];
  }

  clearFilters(): void {
    this.nameFilter.setValue('');
    this.surnameFilter.setValue('');
  }

  toggleViewMode(): void {
    this.viewMode = this.viewMode === 'grid' ? 'list' : 'grid';
  }

  selectDriver(driver: Driver): void {
    this.selectedDriver = driver;
  }
  addDriver(): void {
    this.addDriverModal = true;
    this.resetForm();
  }


  closeDriverModal(): void {
    this.addDriverModal = false;
    this.selectedDriver = null;
  }

  resetForm(): void {
    this.driverForm.reset({
      active: true
    });
    this.formSubmitted = false;
    this.formErrors = {};
  }

  static passwordMatchValidator(group: FormGroup): { [key: string]: any } | null {
    const password = group.get('password');
    const confirmPassword = group.get('password_confirm');

    if (!password || !confirmPassword) return null;

    return password.value === confirmPassword.value ? null : { 'passwordMismatch': true };
  }

  saveDriver(): void {
    this.formSubmitted = true;

    if (this.driverForm.invalid) {
  
      Object.keys(this.driverForm.controls).forEach(key => {
        this.driverForm.get(key)?.markAsTouched();
      });
      return;
    }

    const driverData: any = {
      name: this.driverForm.value.name,
      surname: this.driverForm.value.surname,
      username: this.driverForm.value.username,
      email: this.driverForm.value.email,
      password: this.driverForm.value.password,
      password_conifrm: this.driverForm.value.password_confirm,
      telephone_number: this.driverForm.value.telephone_number,
      gender: this.driverForm.value.gender,
      active: this.driverForm.value.active
    };
    console.log(driverData);
    this.driverService.create(driverData).subscribe({
      next: (response) => {
        this.closeDriverModal();
        this.loadDrivers();
      },
      error: (error) => {
        console.error('Error creating driver:', error);
        if (error.error && typeof error.error === 'object') {
          this.formErrors = error.error;
        } else {
          this.formErrors = { general: 'An error occurred while creating the driver' };
        }
      }
    });
  }
  confirmDelete(driver: Driver, event?: Event): void {
    if (event) {
      event.stopPropagation();
    }
    this.driverToDelete = driver;
    this.showDeleteConfirmation = true;
  }

  cancelDelete(): void {
    this.driverToDelete = null;
    this.showDeleteConfirmation = false;
  }

  deleteDriver(): void {
    if (!this.driverToDelete) return;

    this.driverService.delete(this.driverToDelete.did!).subscribe({
      next: () => {
        this.loadDrivers();
        this.showDeleteConfirmation = false;
        this.driverToDelete = null;
      },
      error: (err: any) => {
        console.log(err);
      }
    });
  }
}
