import { Component, OnInit } from '@angular/core';
import { MasterComponent } from '../master/master.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DriverService } from '../../services/driver.service';
import { Driver } from '../../models/driver';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
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
  viewMode: 'grid' | 'list' = 'grid';

  constructor(private driverService: DriverService) { }

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

  closeDriverDetails(): void {
    this.selectedDriver = null;
  }
}