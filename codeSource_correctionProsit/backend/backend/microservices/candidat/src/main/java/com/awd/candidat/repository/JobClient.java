package com.awd.candidat.repository;

import com.awd.candidat.dto.JobDTO;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;
@FeignClient(name = "job", url = "http://localhost:8082")
public interface JobClient {
    @GetMapping("/api/jobs")
    List<JobDTO> findAll();

    @GetMapping("/api/jobs/{id}")
    JobDTO findById(@PathVariable("id") Long id);
}


