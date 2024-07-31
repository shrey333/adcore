import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { CourseService } from '../course.service';
import { Course } from '../course.model';
import { Router } from '@angular/router';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-course-list',
  templateUrl: './course-list.component.html',
  styleUrls: ['./course-list.component.css'],
})
export class CourseListComponent implements OnInit {
  displayedColumns: string[] = [
    'CourseName',
    'Location',
    'Start',
    'Length',
    'Price',
    'actions',
  ];
  dataSource = new MatTableDataSource<Course>();
  totalCourses = 0;
  pageSize = 10;
  currentPage = 0;
  pageSizeOptions: number[] = [5, 10, 25, 50];
  searchControl = new FormControl('');

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    public courseService: CourseService,
    public router: Router,
  ) {}

  ngOnInit(): void {
    this.loadCourses();
    this.searchControl.valueChanges.subscribe(() => {
      this.loadCourses();
    });
  }

  calculateCourseLength(startDate: Date, endDate: Date): number {
    const start = new Date(startDate);
    const end = new Date(endDate);
    return Math.ceil((end.getTime() - start.getTime()) / (1000 * 3600 * 24));
  }

  formatPrice(price: number, currency: string): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
    }).format(price);
  }

  loadCourses(page: number = 0, size: number = this.pageSize) {
    const search = this.searchControl.value;
    this.courseService
      .getCourses(search || '', page + 1, size)
      .subscribe((data) => {
        this.dataSource.data = data.courses.map((course: any) => ({
          ...course,
          CourseLength: this.calculateCourseLength(
            course.StartDate,
            course.EndDate,
          ),
          FormattedPrice: this.formatPrice(course.Price, course.Currency),
        }));
        this.totalCourses = data.total;
      });
  }

  onPageChange(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.currentPage = event.pageIndex;
    this.loadCourses(this.currentPage, this.pageSize);
  }

  editCourse(course: Course) {
    this.router.navigate([`/course/edit/${course._id}`], { state: { course } });
  }

  deleteCourse(id: string) {
    this.courseService.deleteCourse(id).subscribe(() => {
      this.loadCourses(this.currentPage, this.pageSize);
    });
  }
}
