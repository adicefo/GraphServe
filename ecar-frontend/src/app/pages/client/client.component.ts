import { Component, OnInit } from '@angular/core';
import { MasterComponent } from '../master/master.component';
import { SearchResult } from '../../models/search_result';
import { Client } from '../../models/client';
import { FormControl, FormGroup, Validators,AbstractControlOptions, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ClientService } from '../../services';
import { CommonModule } from '@angular/common';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

@Component({
  selector: 'app-client',
  imports: [MasterComponent, CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './client.component.html',
  styleUrl: './client.component.css'
})
export class ClientComponent implements OnInit{
   clients: SearchResult<Client> = {
    result: [],
    count: 0
  };
  fliteredClients: Client[] = [];
  isLoading: boolean = false;
  error: string | null = null;
  
  nameFilter = new FormControl('');
  surnameFilter = new FormControl('');

  selectedClient:Client |null=null;
  clientToDelete:Client |null=null;
  showDeleteConfirmation=false;
  viewMode: 'grid' | 'list' = 'grid';

  addClientModal:boolean=false;


  clientForm: FormGroup;
  formSubmitted = false;
  formErrors: any = {};

  constructor(private clientService: ClientService) {
    this.clientForm = new FormGroup({
      name: new FormControl('', [Validators.required]),
      surname: new FormControl('', [Validators.required]),
      username: new FormControl('', [Validators.required, Validators.minLength(5)]),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required]),
      password_confirm: new FormControl('', [Validators.required]),
      telephone_number: new FormControl('', [Validators.required]),
      gender: new FormControl('', [Validators.required]),
      active: new FormControl(true)
    }, { validators: ClientComponent.passwordMatchValidator } as AbstractControlOptions);
  }
  ngOnInit(): void {
    this.loadClients();

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

  loadClients():void{
    this.isLoading = true;
    this.error = null;

    this.clientService.getAll().subscribe({
      next: (data: SearchResult<Client>) => {
        this.clients = data;
        this.fliteredClients = data.result || [];
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Failed to load clients. Please try again later.';
        this.isLoading = false;
        console.error('Error loading drivers:', err);
      }
    });
  }


  applyFilters(): void {
    const nameValue = this.nameFilter.value?.toLowerCase() || '';
    const surnameValue = this.surnameFilter.value?.toLowerCase() || '';

    this.fliteredClients = this.clients.result?.filter(client => {
      const matchesName = !nameValue ||
        (client.user?.name?.toLowerCase().includes(nameValue));
      const matchesSurname = !surnameValue ||
        (client.user?.surname?.toLowerCase().includes(surnameValue));

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
  selectClient(client: Client): void {
    this.selectedClient = client;
  }
 

  resetForm(): void {
    this.clientForm.reset({
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
  closeClientModal():void{
    this.addClientModal=false;
    this.selectedClient=null;
  }
  addClient():void{
    console.log('addClient');
    this.addClientModal=true;
    this.resetForm();
  }
  saveDriver(): void {
    this.formSubmitted = true;

    if (this.clientForm.invalid) {
  
      Object.keys(this.clientForm.controls).forEach(key => {
        this.clientForm.get(key)?.markAsTouched();
      });
      return;
    }

    const clientData: any = {
      name: this.clientForm.value.name,
      surname: this.clientForm.value.surname,
      username: this.clientForm.value.username,
      email: this.clientForm.value.email,
      password: this.clientForm.value.password,
      password_conifrm: this.clientForm.value.password_confirm,
      telephone_number: this.clientForm.value.telephone_number,
      gender: this.clientForm.value.gender,
      active: this.clientForm.value.active
    };
    console.log(clientData);
    this.clientService.create(clientData).subscribe({
      next: (response) => {
        this.closeClientModal();
        this.loadClients();
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
  confirmDelete(client: Client, event?: Event): void {
    if (event) {
      event.stopPropagation();
    }
    this.clientToDelete = client;
    this.showDeleteConfirmation = true;
  }

  cancelDelete(): void {
    this.clientToDelete = null;
    this.showDeleteConfirmation = false;
  }

  deleteClient(): void {
    if (!this.clientToDelete) return;

    this.clientService.delete(this.clientToDelete.cid!).subscribe({
      next: () => {
        this.loadClients();
        this.showDeleteConfirmation = false;
        this.clientToDelete = null;
      },
      error: (err: any) => {
        console.log(err);
      }
    });
  }
}
