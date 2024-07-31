import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Course } from '../course.model';
import { Observable } from 'rxjs';
import { startWith, map } from 'rxjs/operators';
import { CourseService } from '../course.service';

@Component({
  selector: 'app-course-form',
  templateUrl: './course-form.component.html',
  styleUrls: ['./course-form.component.css'],
})
export class CourseFormComponent implements OnInit {
  courseForm!: FormGroup;
  isEditMode = false;
  course: Course | null = null;

  filteredUniversities!: Observable<string[]>;
  filteredCities!: Observable<string[]>;
  filteredCountries!: Observable<string[]>;

  universities: string[] = [];
  cities: string[] = [];
  countries: string[] = [];

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private courseService: CourseService,
  ) {}

  ngOnInit(): void {
    this.courseForm = this.fb.group({
      University: ['', Validators.required],
      City: ['', Validators.required],
      Country: ['', Validators.required],
      CourseName: ['', Validators.required],
      CourseDescription: ['', Validators.required],
      StartDate: ['', Validators.required],
      EndDate: ['', Validators.required],
      Price: ['', [Validators.required, Validators.min(0)]],
      Currency: ['', Validators.required],
    });

    const state = history.state;
    if (state && state.course) {
      this.course = state.course;
      this.isEditMode = true;
      this.courseForm.patchValue({
        ...this.course,
      });
    }

    this.filteredUniversities = this.courseForm
      .get('University')!
      .valueChanges.pipe(
        startWith(''),
        map((value) => this._filter(value, 'university')),
      );

    this.filteredCities = this.courseForm.get('City')!.valueChanges.pipe(
      startWith(''),
      map((value) => this._filter(value, 'city')),
    );

    this.filteredCountries = this.courseForm.get('Country')!.valueChanges.pipe(
      startWith(''),
      map((value) => this._filter(value, 'country')),
    );

    this.loadAllData();
  }

  private _filter(value: string, type: string): string[] {
    const filterValue = value.toLowerCase();
    let data: string[] = [];
    switch (type) {
      case 'university':
        data = this.universities;
        break;
      case 'city':
        data = this.cities;
        break;
      case 'country':
        data = this.countries;
        break;
    }
    return data.filter((option) => option.toLowerCase().includes(filterValue));
  }

  loadAllData() {
    this.courseService.getCourses().subscribe((data) => {
      this.universities = Array.from(
        new Set(data.courses.map((course: Course) => course.University)),
      );
      this.cities = Array.from(
        new Set(data.courses.map((course: Course) => course.City)),
      );
      this.countries = Array.from(
        new Set(data.courses.map((course: Course) => course.Country)),
      );
    });
  }

  onSubmit(): void {
    if (this.courseForm.invalid) {
      return;
    }

    const formValues = this.courseForm.value;
    const course: Course = {
      ...formValues,
      StartDate: this.formatDate(formValues.StartDate),
      EndDate: this.formatDate(formValues.EndDate),
    };

    if (this.isEditMode && this.course) {
      this.courseService
        .updateCourse(this.course._id!, course)
        .subscribe(() => {
          this.router.navigate(['/']);
        });
    } else {
      this.courseService.createCourse(course).subscribe(() => {
        this.router.navigate(['/']);
      });
    }
  }

  formatDate(date: any): string {
    const d = new Date(date);
    return `${d.getFullYear()}-${this.pad(d.getMonth() + 1)}-${this.pad(d.getDate())}`;
  }

  pad(n: number): string {
    return n < 10 ? '0' + n : n.toString();
  }

  onCancel(): void {
    this.router.navigate(['/']);
  }
}
